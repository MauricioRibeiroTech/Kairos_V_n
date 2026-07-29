import os
import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------
# 1. CONFIGURAÇÃO DA PÁGINA & ESTILO DARK THEME (CSS)
# --------------------------------------------
st.set_page_config(
    page_title="Dashboard Educacional - CTV",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Injeção de CSS para um Dark Theme elegante
st.markdown("""
<style>
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    
    section[data-testid="stSidebar"] {
        background-color: #161b22 !important;
        border-right: 1px solid #30363d;
    }
    
    div[data-testid="stMetric"] {
        background-color: #161b22 !important;
        border: 1px solid #30363d !important;
        border-radius: 10px !important;
        padding: 15px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3) !important;
    }
    
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 800 !important;
        color: #58a6ff !important;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem !important;
        color: #8b949e !important;
        font-weight: 600 !important;
    }
    
    h1 {
        color: #f0f6fc !important;
        font-weight: 800 !important;
        letter-spacing: -0.5px;
    }
    h2, h3 {
        color: #58a6ff !important;
        font-weight: 700 !important;
    }
    
    hr {
        border-color: #30363d !important;
        margin: 1.2rem 0;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------
# 2. CARREGAMENTO DIRETO E ANONIMIZAÇÃO DOS DADOS
# --------------------------------------------
@st.cache_data(ttl=3600)
def carregar_dados_direto():
    """
    Lê os dados locais, oculta os nomes reais e gera IDs anônimos para proteção de privacidade.
    """
    df_m, df_t = pd.DataFrame(), pd.DataFrame()

    if os.path.exists("estudantes_manha.csv"):
        df_m = pd.read_csv("estudantes_manha.csv")
    if os.path.exists("estudantes_tarde.csv"):
        df_t = pd.read_csv("estudantes_tarde.csv")
        
    if df_m.empty and df_t.empty and os.path.exists("dados_alunos.csv"):
        df_unico = pd.read_csv("dados_alunos.csv")
        if 'Turno' in df_unico.columns:
            df_m = df_unico[df_unico['Turno'] == 'Manhã'].copy()
            df_t = df_unico[df_unico['Turno'] == 'Tarde'].copy()
        else:
            df_m = df_unico.copy()

    def tratar_tabela(df, turno):
        if df.empty:
            return pd.DataFrame()

        mapeamento = {
            'COL 1': 'Nome', 'COL 2': 'Curso', 'COL 3': 'Serie',
            'COL 4': 'Turma', 'COL 5': 'Deficiencia', 'COL 6': 'Especificacao',
            'COL 7': 'Situacao', 'COL 8': 'Observacao'
        }
        colunas_existentes = {k: v for k, v in mapeamento.items() if k in df.columns}
        df = df.rename(columns=colunas_existentes)

        df = df.rename(columns={'Seriacao': 'Serie', 'Especificação': 'Especificacao', 'Situação': 'Situacao'})

        cabecalhos = ['Nome', 'ESTUDANTES  MANHÃ', 'ESTUDANTES TARDE', ' \\', '']
        if 'Nome' in df.columns:
            df = df[~df['Nome'].isin(cabecalhos)]
            df = df[df['Nome'].notna()]

        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].astype(str).str.strip()

        df['Turno'] = turno

        sem_laudo = ['S/L', 'Sem laudo', '', 'nan', 'None']
        if 'Especificacao' in df.columns:
            df['Com_Laudo'] = ~df['Especificacao'].isin(sem_laudo) & df['Especificacao'].notna()
        else:
            df['Com_Laudo'] = False

        return df

    df_m = tratar_tabela(df_m, 'Manhã')
    df_t = tratar_tabela(df_t, 'Tarde')

    df_total = pd.concat([df_m, df_t], ignore_index=True) if not df_m.empty or not df_t.empty else pd.DataFrame()
    
    # anonimização: Substitui os nomes por IDs numéricos sequenciais
    if not df_total.empty:
        df_total = df_total.drop(columns=['Nome'], errors='ignore') # Remove a coluna original de Nomes
        df_total.insert(0, 'ID Estudante', [f"EST-{i+1:03d}" for i in range(len(df_total))])
        
        # Atualiza os DataFrames de turno com base no total anonimizado
        df_m = df_total[df_total['Turno'] == 'Manhã'].copy()
        df_t = df_total[df_total['Turno'] == 'Tarde'].copy()

    return df_total, df_m, df_t


# Executa o carregamento dos dados com segurança e privacidade
df_total, df_manha, df_tarde = carregar_dados_direto()


# --------------------------------------------
# 3. BARRA LATERAL (FILTROS)
# --------------------------------------------
st.sidebar.title("⚙️ Filtros do Sistema")

turno_selecionado = st.sidebar.radio("Turno", ['Todos', 'Manhã', 'Tarde'], index=0)

if turno_selecionado == 'Manhã':
    df_filtrado = df_manha.copy()
elif turno_selecionado == 'Tarde':
    df_filtrado = df_tarde.copy()
else:
    df_filtrado = df_total.copy()

# Busca por ID Anônimo
busca_id = st.sidebar.text_input("🔍 Pesquisar por ID Estudante (ex: EST-005)", "")
if busca_id:
    df_filtrado = df_filtrado[df_filtrado['ID Estudante'].str.contains(busca_id, case=False, na=False)]

# Filtros Dinâmicos
if not df_filtrado.empty:
    series_opcoes = sorted([s for s in df_filtrado['Serie'].dropna().unique() if s != 'nan'])
    serie_sel = st.sidebar.multiselect("Série", series_opcoes, default=series_opcoes)

    defic_opcoes = sorted([d for d in df_filtrado['Deficiencia'].dropna().unique() if d != 'nan'])
    defic_sel = st.sidebar.multiselect("Deficiência", defic_opcoes, default=defic_opcoes)

    sit_opcoes = sorted([s for s in df_filtrado['Situacao'].dropna().unique() if s != 'nan'])
    sit_sel = st.sidebar.multiselect("Situação", sit_opcoes, default=sit_opcoes)

    apenas_laudo = st.sidebar.checkbox("Apenas Alunos com Laudo", value=True)

    if serie_sel:
        df_filtrado = df_filtrado[df_filtrado['Serie'].isin(serie_sel)]
    if defic_sel:
        df_filtrado = df_filtrado[df_filtrado['Deficiencia'].isin(defic_sel)]
    if sit_sel:
        df_filtrado = df_filtrado[df_filtrado['Situacao'].isin(sit_sel)]
    if apenas_laudo:
        df_filtrado = df_filtrado[df_filtrado['Com_Laudo'] == True]


# --------------------------------------------
# 4. PAINEL PRINCIPAL & MÉTRICAS
# --------------------------------------------
st.title("🎓 Painel Educacional de Inclusão - CTV")
st.markdown("Monitoramento estratégico de inclusão com **identidade preservada (LGPD)**.")
st.markdown("---")

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Exibido", len(df_filtrado))
m2.metric("Com Laudo", len(df_filtrado[df_filtrado['Com_Laudo'] == True]) if 'Com_Laudo' in df_filtrado.columns else 0)
m3.metric("Manhã", len(df_filtrado[df_filtrado['Turno'] == 'Manhã']) if 'Turno' in df_filtrado.columns else 0)
m4.metric("Tarde", len(df_filtrado[df_filtrado['Turno'] == 'Tarde']) if 'Turno' in df_filtrado.columns else 0)

st.markdown("---")


# --------------------------------------------
# 5. GRÁFICOS ANALÍTICOS (DARK MODE PLOTLY)
# --------------------------------------------
st.subheader("📊 Diagnóstico e Distribuições")

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
                title='<b>Deficiências Identificadas</b>',
                text='Alunos',
                color='Alunos',
                color_continuous_scale='teal',
                template='plotly_dark'
            )
            fig_def.update_layout(yaxis={'categoryorder':'total ascending'}, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_def, use_container_width=True)

    with g2:
        if 'Situacao' in df_filtrado.columns and not df_filtrado['Situacao'].empty:
            df_sit = df_filtrado['Situacao'].value_counts().reset_index()
            df_sit.columns = ['Situação', 'Alunos']
            fig_sit = px.pie(
                df_sit,
                names='Situação',
                values='Alunos',
                title='<b>Situação do Atendimento (SRM)</b>',
                hole=0.45,
                color_discrete_sequence=px.colors.qualitative.Dark24,
                template='plotly_dark'
            )
            fig_sit.update_traces(textinfo='percent+value')
            fig_sit.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_sit, use_container_width=True)

    if 'Serie' in df_filtrado.columns and not df_filtrado['Serie'].empty:
        df_serie = df_filtrado['Serie'].value_counts().reset_index()
        df_serie.columns = ['Série', 'Alunos']
        fig_serie = px.bar(
            df_serie,
            x='Série',
            y='Alunos',
            title='<b>Quantidade de Estudantes por Série</b>',
            text='Alunos',
            color_discrete_sequence=['#58a6ff'],
            template='plotly_dark'
        )
        fig_serie.update_traces(textposition='outside')
        fig_serie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_serie, use_container_width=True)

else:
    st.warning("⚠️ Nenhum registro localizado com os filtros selecionados.")

st.markdown("---")


# --------------------------------------------
# 6. TABELA DE DADOS ANONIMIZADA
# --------------------------------------------
st.subheader("📋 Tabela de Registros Anônimos")

if not df_filtrado.empty:
    cols_exibir = [c for c in ['ID Estudante', 'Curso', 'Serie', 'Turma', 'Deficiencia', 'Especificacao', 'Situacao', 'Turno', 'Observacao'] if c in df_filtrado.columns]
    
    st.dataframe(
        df_filtrado[cols_exibir],
        use_container_width=True,
        hide_index=True
    )

st.markdown("---")
st.caption("🔒 Dados anonimizados em conformidade com as diretrizes de privacidade de dados.")
