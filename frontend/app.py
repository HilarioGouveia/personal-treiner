import streamlit as st
from utils.styles import aplicar_estilo_tech_minimalista
from services import demo

st.set_page_config(
    page_title="Gestão - Personal Trainer", page_icon="🏋️‍♂️", layout="wide"
)

# Aplicar o tema visual customizado
aplicar_estilo_tech_minimalista()
demo.mostrar_aviso()


# Inicializa o estado de autenticação
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False

if not st.session_state.logged_in and not demo.ativo():
  st.title("🔐 Acesso ao Sistema")
  st.subheader("Faça login para gerenciar sua consultoria")

  with st.form("login_form"):
    email = st.text_input("E-mail")
    senha = st.text_input("Senha", type="password")
    submit = st.form_submit_button("Entrar")

    if submit:
      # Validação simples para o MVP (integrado posteriormente com /auth/login)
      if email == "personal@email.com" and senha == "admin123":
        st.session_state.logged_in = True
        st.success("Login realizado com sucesso! Carregando...")
        st.rerun()
      else:
        st.error("E-mail ou senha inválidos.")
else:
  st.title("Painel de Controle - Personal Trainer")
  st.write(
      "Bem-vindo de volta! Utilize o menu lateral para navegar entre os"
      " módulos de Alunos, Treinos e Financeiro."
  )

  if not demo.ativo() and st.button("Sair / Logout"):
    st.session_state.logged_in = False
    st.rerun()
