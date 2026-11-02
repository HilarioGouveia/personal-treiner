import streamlit as st
from services.api_client import criar_aluno, get_alunos
from utils.styles import aplicar_estilo_tech_minimalista
from services.demo import mostrar_aviso

st.set_page_config(
    page_title="Gestão de Alunos", page_icon="👥", layout="wide"
)


# Aplicar o tema visual customizado
aplicar_estilo_tech_minimalista()

st.title("👥 Gestão de Alunos")
mostrar_aviso()

# Abas na interface
aba_lista, aba_cadastro = st.tabs(["📋 Alunos Cadastrados", "➕ Novo Aluno"])

with aba_lista:
  st.subheader("Lista de Alunos Ativos")
  alunos = get_alunos()

  if alunos:
    for aluno in alunos:
      with st.expander(f"📌 {aluno['nome']} - Objetivo: {aluno['objetivo'] or 'Não definido'}"):
        st.write(f"**E-mail:** {aluno.get('email', 'Não informado')}")
        st.write(f"**Telefone:** {aluno.get('telefone', 'Não informado')}")
        st.write(f"**Observações Médicas:** {aluno.get('observacoes_medicas', 'Nenhuma')}")
  else:
    st.info(
        "Nenhum aluno cadastrado ainda ou API offline. Cadastre o primeiro"
        " aluno na aba ao lado."
    )

with aba_cadastro:
  st.subheader("Cadastrar Novo Aluno")

  with st.form("form_novo_aluno"):
    col1, col2 = st.columns(2)
    with col1:
      nome = st.text_input("Nome Completo *")
      email = st.text_input("E-mail de Acesso *")
      senha = st.text_input("Senha Temporária *", type="password")
    with col2:
      telefone = st.text_input("Telefone / WhatsApp")
      data_nascimento = st.date_input("Data de Nascimento", format="DD/MM/YYYY")
      objetivo = st.text_input("Objetivo Principal (Ex: Hipertrofia)")

    observacoes_medicas = st.text_area(
        "Observações Médicas / Restrições (PAR-Q)"
    )

    submitted = st.form_submit_button("Salvar Aluno")

    if submitted:
      if not nome or not email or not senha:
        st.error("Preencha todos os campos obrigatórios (*).")
      else:
        payload = {
            "nome": nome,
            "email": email,
            "senha": senha,
            "telefone": telefone,
            "data_nascimento": str(data_nascimento),
            "objetivo": objetivo,
            "observacoes_medicas": observacoes_medicas,
        }
        response = criar_aluno(payload)
        if response is not None and response.status_code == 201:
          st.success(f"Aluno {nome} cadastrado com sucesso!")
        elif response is None:
          st.error("Não foi possível conectar à API ou o tempo de resposta foi excedido.")
        else:
          try:
            detalhe = response.json().get("detail")
          except (ValueError, AttributeError):
            detalhe = None
          if isinstance(detalhe, str) and response.status_code < 500:
            st.error(f"Erro ao cadastrar aluno: {detalhe}")
          else:
            st.error(f"Erro ao cadastrar aluno (HTTP {response.status_code}). Verifique os logs da API.")
