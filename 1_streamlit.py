import os
import io
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA & ESTILO CSS
# --------------------------------------------
st.set_page_config(
    page_title="Dashboard Educacional - CTV",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Customização CSS para um visual moderno e limpo
st.markdown("""
<style>
    /* Fundo suave para o aplicativo */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Estilização dos Cards de Métricas */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        color: #1e293b;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        color: #64748b !important;
        font-weight: 600 !important;
    }
    
    /* Headers com tipografia elegante */
    h1 {
        color: #0f172a;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    h2, h3 {
        color: #1e293b;
        font-weight: 700 !important;
    }
    
    /* Separador fino estilizado */
    hr {
        margin: 1rem 0;
        border-color: #e2e8f0;
    }
    
    /* Ajustes na sidebar */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------
# 2. FUNÇÃO DE CARREGAMENTO E TRATAMENTO
# --------------------------------------------
@st.cache_data(ttl=3600)
def carregar_dados():
    """
    Carrega os dados dos arquivos CSV locais ('estudantes_manha.csv' e 'estudantes_tarde.csv')
    ou de um CSV único ('dados_alunos.csv'). Trata nulos, mapeia colunas e identifica laudos.
    """
    df_manha = pd.DataFrame()
    df_tarde = pd.DataFrame()
    
    # Tentativa 1: Arquivos CSV separados por turno
    if os.path.exists("estudantes_manha.csv") and os.path.exists("estudantes_tarde.csv"):
        df_manha = pd.read_csv("estudantes_manha.csv")
        df_tarde = pd.read_csv("estudantes_tarde.csv")
    # Tentativa 2: Arquivo CSV único consolidado
    elif os.path.exists("dados_alunos.csv"):
        df_unico = pd.read_csv("dados_alunos.csv")
        if 'Turno' in df_unico.columns:
            df_manha = df_unico[df_unico['Turno'] == 'Manhã'].copy()
            df_tarde = df_unico[df_unico['Turno'] == 'Tarde'].copy()
        else:
            df_manha = df_unico.copy()

    def tratar_tabela(df, turno):
        if df.empty:
            return pd.DataFrame()

        # Mapeamento dinâmico de colunas
        mapeamento = {
            'COL 1': 'Nome',
            'COL 2': 'Curso',
            'COL 3': 'Serie',
            'COL 4': 'Turma',
            'COL 5': 'Deficiencia',
            'COL 6': 'Especificacao',
            'COL 7': 'Situacao'
        }
        if turno == 'Manhã':
            mapeamento['COL 8'] = 'Observacao'

        # Renomeia colunas se a estrutura for do tipo SQL (COL 1, COL 2...)
        colunas_existentes = {k: v for k, v in mapeamento.items() if k in df.columns}
        df = df.rename(columns=colunas_existentes)

        # Se já tiver nomes padronizados, garante que existem
        if 'Seriacao' in df.columns and 'Serie' not in df.columns:
            df = df.rename(columns={'Seriacao': 'Serie'})
        if 'Especificação' in df.columns and 'Especificacao' not in df.columns:
            df = df.rename(columns={'Especificação': 'Especificacao'})
        if 'Situação' in df.columns and 'Situacao' not in df.columns:
            df = df.rename(columns={'Situação': 'Situacao'})

        # Remoção de cabeçalhos acidentais inseridos como linhas
        cabecalhos_invalidos = ['Nome', 'ESTUDANTES  MANHÃ', 'ESTUDANTES TARDE', ' \\', '']
        if 'Nome' in df.columns:
            df = df[~df['Nome'].isin(cabecalhos_invalidos)]
            df = df[df['Nome'].notna()]

        # Limpeza de espaços em branco adicionais
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].astype(str).str.strip()

        df['Turno'] = turno

        # Identificação de Laudo
        sem_laudo_valores = ['S/L', 'Sem laudo', '', 'nan', 'None']
        if 'Especificacao' in df.columns:
            df['Com_Laudo'] = ~df['Especificacao'].isin(sem_laudo_valores) & df['Especificacao'].notna()
        else:
            df['Com_Laudo'] = False

        return df

    df_m = tratar_tabela(df_manha, 'Manhã')
    df_t = tratar_tabela(df_tarde, 'Tarde')

    df_total = pd.concat([df_m, df_t], ignore_index=True) if not df_m.empty or not df_t.empty else pd.DataFrame()
    return df_total, df_m, df_t


# --------------------------------------------
# 3. CARREGAMENTO & FALLBACK DE UPLOAD
# --------------------------------------------
df_total, df_manha, df_tarde = carregar_dados()

# Interface de Contingência/Upload caso não encontre os CSVs no repositório
if df_total.empty:
    st.info("📂 **Nenhum arquivo CSV detectado na raiz do repositório.**")
    st.markdown("Para visualizar a aplicação, faça o upload dos seus arquivos CSV abaixo:")
    
    col_up1, col_up2 = st.columns(2)
    with col_up1:
        up_m = st.file_uploader("Upload: Estudantes Manhã (CSV)", type=['csv'], key="up_m")
    with col_up2:
        up_t = st.file_uploader("Upload: Estudantes Tarde (CSV)", type=['csv'], key="up_t")

    if up_m or up_t:
        df_m_raw = pd.read_csv(up_m) if up_m else pd.DataFrame()
        df_t_raw = pd.read_csv(up_t) if up_t else pd.DataFrame()
        
        # Reprocessa os arquivos enviados
        def tratar_upload(df, turno):
            if df.empty:
                return pd.DataFrame()
            df['Turno'] = turno
            if 'Especificacao' in df.columns:
                df['Com_Laudo'] = ~df['Especificacao'].isin(['S/L', 'Sem laudo', '']) & df['Especificacao'].notna()
            return df

        df_manha = tratar_upload(df_m_raw, 'Manhã')
        df_tarde = tratar_upload(df_t_raw, 'Tarde')
        df_total = pd.concat([df_manha, df_tarde], ignore_index=True)
    else:
        st.stop()


# --------------------------------------------
# 4. BARRA LATERAL (FILTROS INTERATIVOS)
# --------------------------------------------
st.sidebar.title("⚙️ Painel de Controle")
st.sidebar.markdown("Filtre as informações em tempo real:")

# Filtro por Turno
turno_selecionado = st.sidebar.radio("Selecione o Turno", ['Todos', 'Manhã', 'Tarde'], index=0)

if turno_selecionado == 'Manhã':
    df_filtrado = df_manha.copy()
elif turno_selecionado == 'Tarde':
    df_filtrado = df_tarde.copy()
else:
    df_filtrado = df_total.copy()

# Busca textual por Nome
busca_nome = st.sidebar.text_input("🔍 Buscar por Nome do Aluno", "")
if busca_nome:
    df_filtrado = df_filtrado[df_filtrado['Nome'].str.contains(busca_nome, case=False, na=False)]

# Filtro por Série
series_opcoes = sorted([s for s in df_filtrado['Serie'].dropna().unique() if s != 'nan'])
serie_sel = st.sidebar.multiselect("Série", series_opcoes, default=series_opcoes)

# Filtro por Deficiência
defic_opcoes = sorted([d for d in df_filtrado['Deficiencia'].dropna().unique() if d != 'nan'])
defic_sel = st.sidebar.multiselect("Deficiência", defic_opcoes, default=defic_opcoes)

# Filtro por Situação
sit_opcoes = sorted([s for s in df_filtrado['Situacao'].dropna().unique() if s != 'nan'])
sit_sel = st.sidebar.multiselect("Situação do Aluno", sit_opcoes, default=sit_opcoes)

# Checkbox Laudo
apenas_laudo = st.sidebar.checkbox("Exibir apenas alunos com Laudo", value=True)

# Aplicação dos Filtros Selecionados
if serie_sel:
    df_filtrado = df_filtrado[df_filtrado['Serie'].isin(serie_sel)]
if defic_sel:
    df_filtrado = df_filtrado[df_filtrado['Deficiencia'].isin(defic_sel)]
if sit_sel:
    df_filtrado = df_filtrado[df_filtrado['Situacao'].isin(sit_sel)]
if apenas_laudo:
    df_filtrado = df_filtrado[df_filtrado['Com_Laudo'] == True]


# --------------------------------------------
# 5. CABEÇALHO & CARDS DE MÉTRICAS
# --------------------------------------------
st.title("🎓 Painel Educacional de Inclusão - CTV")
st.markdown("Acompanhamento analítico dos estudantes com laudos e necessidades específicas de aprendizagem.")
st.markdown("---")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total de Alunos (Filtro)", len(df_filtrado))
m2.metric("Com Laudo Técnico", len(df_filtrado[df_filtrado['Com_Laudo'] == True]))
m3.metric("Turno Manhã", len(df_filtrado[df_filtrado['Turno'] == 'Manhã']))
m4.metric("Turno Tarde", len(df_filtrado[df_filtrado['Turno'] == 'Tarde']))

st.markdown("---")


# --------------------------------------------
# 6. GRÁFICOS ANALÍTICOS (PLOTLY INTERATIVO)
# --------------------------------------------
st.subheader("📊 Visualizações e Diagnósticos")

if not df_filtrado.empty:
    g1, g2 = st.columns(2)

    with g1:
        if 'Deficiencia' in df_filtrado.columns and not df_filtrado['Deficiencia'].empty:
            df_def = df_filtrado['Deficiencia'].value_counts().reset_index()
            df_def.columns = ['Deficiência', 'Alunos']
            fig_def = px.bar(
                df_def,
                x='Alunos',
                y='Deficiência',
                orientation='h',
                title='<b>Distribuição por Tipo de Deficiência</b>',
                text='Alunos',
                color='Alunos',
                color_continuous_scale='Viridis'
            )
            fig_def.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_def, use_container_width=True)

    with g2:
        if 'Situacao' in df_filtrado.columns and not df_filtrado['Situacao'].empty:
            df_sit = df_filtrado['Situacao'].value_counts().reset_index()
            df_sit.columns = ['Situação', 'Alunos']
            fig_sit = px.pie(
                df_sit,
                names='Situação',
                values='Alunos',
                title='<b>Situação do Atendimento (SRM/Atendimento)</b>',
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            fig_sit.update_traces(textinfo='percent+value')
            fig_sit.update_layout(margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_sit, use_container_width=True)

    # Gráfico de Distribuição por Série
    if 'Serie' in df_filtrado.columns and not df_filtrado['Serie'].empty:
        df_serie = df_filtrado['Serie'].value_counts().reset_index()
        df_serie.columns = ['Série', 'Alunos']
        fig_serie = px.bar(
            df_serie,
            x='Série',
            y='Alunos',
            title='<b>Volume de Alunos por Série</b>',
            text='Alunos',
            color_discrete_sequence=['#2563eb']
        )
        fig_serie.update_traces(textposition='outside')
        fig_serie.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig_serie, use_container_width=True)

else:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")

st.markdown("---")


# --------------------------------------------
# 7. TABELA DE DADOS INTERATIVA
# --------------------------------------------
st.subheader("📋 Listagem Detalhada de Alunos")

if not df_filtrado.empty:
    cols_exibir = [c for c in ['Nome', 'Curso', 'Serie', 'Turma', 'Deficiencia', 'Especificacao', 'Situacao', 'Turno', 'Observacao'] if c in df_filtrado.columns]
    
    st.dataframe(
        df_filtrado[cols_exibir],
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Ajuste os filtros na barra lateral para visualizar os dados.")


# --------------------------------------------
# 8. EXPORTAÇÃO DE DADOS & RODAPÉ
# --------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Exportar Relatório")

if not df_filtrado.empty:
    cols_exp = [c for c in ['Nome', 'Curso', 'Serie', 'Turma', 'Deficiencia', 'Especificacao', 'Situacao', 'Turno', 'Observacao'] if c in df_filtrado.columns]
    buffer = io.BytesIO()
    df_filtrado[cols_exp].to_csv(buffer, index=False, encoding='utf-8-sig')
    
    st.sidebar.download_button(
        label="📄 Baixar Relatório (CSV)",
        data=buffer.getvalue(),
        file_name="relatorio_alunos_laudo.csv",
        mime="text/csv"
    )

st.markdown("---")
st.caption("🚀 Dashboard otimizado para alta performance via dados CSV | Atualizado para Streamlit Cloud")
