import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine, text
import pymysql

# --------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# --------------------------------------------
st.set_page_config(
    page_title="📋 Alunos com Laudo - CTV",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------
# CONFIGURAÇÕES DE CONEXÃO (edite aqui)
# --------------------------------------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mauricio',
    'database': 'cadastro',
    'port': 3306,
    'charset': 'utf8mb4'
}

# --------------------------------------------
# FUNÇÃO DE CARREGAMENTO (com cache)
# --------------------------------------------
@st.cache_data(ttl=600)
def carregar_dados():
    """
    Carrega dados das duas tabelas e retorna um DataFrame único,
    já com a coluna 'Turno' e a classificação 'Com_Laudo'.
    """
    engine = None
    try:
        engine = create_engine(
            f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset={DB_CONFIG['charset']}"
        )
    except Exception as e:
        st.error(f"❌ Erro ao criar engine de conexão: {e}")
        return pd.DataFrame(), pd.DataFrame()

    def _carregar_tabela(nome_tabela, turno):
        """Carrega uma tabela completa, renomeia colunas e filtra cabeçalhos."""
        query = f"SELECT * FROM {nome_tabela}"
        try:
            with engine.connect() as conn:
                df = pd.read_sql(text(query), conn)
        except Exception as e:
            st.warning(f"⚠️ Não foi possível carregar a tabela {nome_tabela}: {e}")
            # Retorna DataFrame vazio com as colunas esperadas
            if turno == 'Manhã':
                cols = ['COL 1','COL 2','COL 3','COL 4','COL 5','COL 6','COL 7','COL 8']
            else:
                cols = ['COL 1','COL 2','COL 3','COL 4','COL 5','COL 6','COL 7']
            return pd.DataFrame(columns=cols)

        # Renomeia as colunas
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
        # Renomeia apenas as colunas que existem
        colunas_existentes = {k: v for k, v in mapeamento.items() if k in df.columns}
        df.rename(columns=colunas_existentes, inplace=True)

        # Remove linhas de cabeçalho (onde Nome está em uma lista de strings)
        cabecalhos = ['Nome', 'ESTUDANTES  MANHÃ', 'ESTUDANTES TARDE', ' \\', '']
        df = df[~df['Nome'].isin(cabecalhos)]
        df = df[df['Nome'].notna()]  # remove nulos

        # Remove espaços extras nas colunas de texto
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].str.strip()

        # Adiciona coluna de turno
        df['Turno'] = turno

        # Define 'Com_Laudo': Especificacao não é nula, vazia, 'S/L' ou 'Sem laudo'
        sem_laudo = ['S/L', 'Sem laudo', '']
        df['Com_Laudo'] = ~df['Especificacao'].isin(sem_laudo) & df['Especificacao'].notna()

        return df

    # Carrega ambas as tabelas
    df_manha = _carregar_tabela('estudantes_manha', 'Manhã')
    df_tarde = _carregar_tabela('estudantes_tarde', 'Tarde')

    # Concatena
    df_total = pd.concat([df_manha, df_tarde], ignore_index=True)
    return df_total, df_manha, df_tarde

# --------------------------------------------
# CARREGAMENTO DOS DADOS
# --------------------------------------------
df_total, df_manha, df_tarde = carregar_dados()

# Fallback para CSV caso não haja dados
if df_total.empty:
    st.info("📂 Nenhum dado encontrado no banco. Você pode carregar um arquivo CSV com a estrutura adequada.")
    uploaded = st.file_uploader("Carregue um CSV (opcional)", type=['csv'])
    if uploaded is not None:
        df_total = pd.read_csv(uploaded)
        # Garante colunas essenciais
        for col in ['Nome', 'Curso', 'Serie', 'Turma', 'Deficiencia', 'Especificacao', 'Situacao', 'Turno', 'Com_Laudo']:
            if col not in df_total.columns:
                df_total[col] = None
        sem_laudo = ['S/L', 'Sem laudo', '']
        df_total['Com_Laudo'] = ~df_total['Especificacao'].isin(sem_laudo) & df_total['Especificacao'].notna()
        if 'Turno' in df_total.columns:
            df_manha = df_total[df_total['Turno'] == 'Manhã'].copy()
            df_tarde = df_total[df_total['Turno'] == 'Tarde'].copy()
        else:
            df_manha = df_total.copy()
            df_tarde = pd.DataFrame(columns=df_total.columns)
    else:
        st.stop()

# --------------------------------------------
# SIDEBAR - FILTROS
# --------------------------------------------
st.sidebar.header("🔍 Filtros")

turno_opcoes = ['Todos', 'Manhã', 'Tarde']
turno_selecionado = st.sidebar.radio("Turno", turno_opcoes, index=0)

if turno_selecionado == 'Manhã':
    df_filtrado_turno = df_manha
elif turno_selecionado == 'Tarde':
    df_filtrado_turno = df_tarde
else:
    df_filtrado_turno = df_total

series_disponiveis = sorted(df_filtrado_turno['Serie'].dropna().unique())
serie_selecionada = st.sidebar.multiselect("Série", series_disponiveis, default=series_disponiveis)

deficiencias = sorted(df_filtrado_turno['Deficiencia'].dropna().unique())
deficiencia_selecionada = st.sidebar.multiselect("Deficiência", deficiencias, default=deficiencias)

situacoes = sorted(df_filtrado_turno['Situacao'].dropna().unique())
situacao_selecionada = st.sidebar.multiselect("Situação", situacoes, default=situacoes)

mostrar_laudo = st.sidebar.checkbox("Mostrar apenas alunos com laudo", value=True)

df_exibicao = df_filtrado_turno.copy()
if serie_selecionada:
    df_exibicao = df_exibicao[df_exibicao['Serie'].isin(serie_selecionada)]
if deficiencia_selecionada:
    df_exibicao = df_exibicao[df_exibicao['Deficiencia'].isin(deficiencia_selecionada)]
if situacao_selecionada:
    df_exibicao = df_exibicao[df_exibicao['Situacao'].isin(situacao_selecionada)]
if mostrar_laudo:
    df_exibicao = df_exibicao[df_exibicao['Com_Laudo'] == True]

# --------------------------------------------
# TÍTULO E MÉTRICAS
# --------------------------------------------
st.title("📋 Alunos com Laudo - CTV")
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de alunos", len(df_total))
with col2:
    st.metric("Com laudo", len(df_total[df_total['Com_Laudo']]))
with col3:
    st.metric("Manhã", len(df_manha))
with col4:
    st.metric("Tarde", len(df_tarde))

st.markdown("---")

# --------------------------------------------
# TABELA
# --------------------------------------------
st.subheader("📄 Lista de Alunos")
if df_exibicao.empty:
    st.info("Nenhum aluno encontrado com os filtros atuais.")
else:
    colunas_exibir = ['Nome', 'Curso', 'Serie', 'Turma', 'Deficiencia', 'Especificacao', 'Situacao', 'Turno']
    if 'Observacao' in df_exibicao.columns:
        colunas_exibir.append('Observacao')
    df_tabela = df_exibicao[colunas_exibir].copy()

    def highlight_laudo(row):
        if mostrar_laudo:
            return ['background-color: #000000'] * len(row)
        else:
            if row.name in df_exibicao[df_exibicao['Com_Laudo']].index:
                return ['background-color: #d4edda'] * len(row)
            return [''] * len(row)

    st.dataframe(
        df_tabela.style.apply(highlight_laudo, axis=1),
        use_container_width=True,
        hide_index=True
    )

# --------------------------------------------
# GRÁFICOS
# --------------------------------------------
st.markdown("---")
st.subheader("📊 Análises")

if not df_exibicao.empty:
    col_graf1, col_graf2 = st.columns(2)
    with col_graf1:
        contagem_def = df_exibicao['Deficiencia'].value_counts().reset_index()
        contagem_def.columns = ['Deficiência', 'Quantidade']
        fig1 = px.bar(
            contagem_def,
            x='Deficiência',
            y='Quantidade',
            color='Deficiência',
            text='Quantidade',
            title='Distribuição por Deficiência'
        )
        fig1.update_traces(textposition='outside')
        fig1.update_layout(showlegend=False)
        st.plotly_chart(fig1, use_container_width=True)

    with col_graf2:
        contagem_sit = df_exibicao['Situacao'].value_counts().reset_index()
        contagem_sit.columns = ['Situação', 'Quantidade']
        fig2 = px.pie(
            contagem_sit,
            values='Quantidade',
            names='Situação',
            title='Distribuição por Situação',
            hole=0.3,
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig2, use_container_width=True)

    contagem_serie = df_exibicao['Serie'].value_counts().reset_index()
    contagem_serie.columns = ['Série', 'Quantidade']
    fig3 = px.bar(
        contagem_serie,
        x='Série',
        y='Quantidade',
        color='Série',
        text='Quantidade',
        title='Distribuição por Série'
    )
    fig3.update_traces(textposition='outside')
    fig3.update_layout(showlegend=False)
    st.plotly_chart(fig3, use_container_width=True)

    if not df_manha.empty and not df_tarde.empty:
        st.subheader("📈 Comparação Manhã vs Tarde")
        df_comp = pd.concat([
            df_manha.assign(Turno='Manhã'),
            df_tarde.assign(Turno='Tarde')
        ], ignore_index=True)
        contagem_turno_def = df_comp.groupby(['Turno', 'Deficiencia']).size().reset_index(name='Quantidade')
        if not contagem_turno_def.empty:
            fig4 = px.bar(
                contagem_turno_def,
                x='Deficiencia',
                y='Quantidade',
                color='Turno',
                barmode='group',
                title='Comparação por Turno e Deficiência',
                color_discrete_sequence=['#1f77b4', '#ff7f0e']
            )
            st.plotly_chart(fig4, use_container_width=True)

# --------------------------------------------
# EXPORTAR
# --------------------------------------------
st.sidebar.markdown("---")
st.sidebar.subheader("📥 Exportar")
if st.sidebar.button("Gerar CSV (filtro atual)"):
    if not df_exibicao.empty:
        csv = df_tabela.to_csv(index=False, encoding='utf-8-sig')
        st.sidebar.download_button(
            label="Clique para baixar",
            data=csv,
            file_name="alunos_filtrados.csv",
            mime="text/csv"
        )
    else:
        st.sidebar.warning("Nenhum dado para exportar.")

st.markdown("---")
st.caption("Dados carregados do banco 'cadastro' - Atualizado em tempo real")
