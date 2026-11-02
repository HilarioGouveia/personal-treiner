"""Navegação lateral com os mesmos ícones usados nas páginas."""
import streamlit as st


def mostrar_navegacao():
    with st.sidebar:
        st.page_link("app.py", label="Início", icon=":material/home:")
        st.page_link("pages/01_Alunos.py", label="Alunos", icon=":material/group:")
        st.page_link("pages/02_Treinos.py", label="Treinos", icon=":material/fitness_center:")
        st.page_link("pages/03_Avaliacoes.py", label="Avaliações", icon=":material/monitoring:")
        st.page_link("pages/04_Financeiro.py", label="Financeiro", icon=":material/account_balance_wallet:")
