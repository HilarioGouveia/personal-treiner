import streamlit as st

st.set_page_config(
    page_title="Gestão - Personal Trainer", page_icon=":material/fitness_center:",
    layout="wide", initial_sidebar_state="auto",
)

pagina = st.navigation([
    st.Page("home.py", title="Início", icon=":material/home:", default=True),
    st.Page("pages/01_Alunos.py", title="Alunos", icon=":material/group:", url_path="Alunos"),
    st.Page("pages/02_Treinos.py", title="Treinos", icon=":material/fitness_center:", url_path="Treinos"),
    st.Page("pages/03_Avaliacoes.py", title="Avaliações", icon=":material/monitoring:", url_path="Avaliacoes"),
    st.Page("pages/04_Financeiro.py", title="Financeiro", icon=":material/account_balance_wallet:", url_path="Financeiro"),
], position="sidebar")
pagina.run()
