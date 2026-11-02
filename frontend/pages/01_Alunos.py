import streamlit as st
from services.api_client import criar_aluno, get_alunos
from utils.styles import aplicar_estilo_tech_minimalista
from services.demo import mostrar_aviso
from utils.navigation import mostrar_navegacao

st.set_page_config(
    page_title="Gestão de Alunos", page_icon=":material/group:", layout="wide"
)


# Aplicar o tema visual customizado
aplicar_estilo_tech_minimalista()

mostrar_navegacao()
st.title("Gestão de Alunos", icon=":material/group:")
mostrar_aviso()

# Abas na interface
aba_lista, aba_cadastro = st.tabs([":material/groups: Alunos Cadastrados", ":material/person_add: Novo Aluno"])

with aba_lista:
  st.subheader("Alunos Cadastrados")
  alunos = get_alunos()

  if alunos:
    linhas = [{"Nome": a["nome"], "Objetivo": a.get("objetivo") or "Não definido",
               "Telefone": a.get("telefone") or "Não informado"} for a in alunos]
    selecao = st.dataframe(
        linhas, hide_index=True, width="stretch", on_select="rerun",
        selection_mode="single-row", key="tabela_alunos_" + "_".join(str(a["id"]) for a in alunos),
    )
    if selecao.selection.rows:
      aluno = alunos[selecao.selection.rows[0]]
      st.subheader(aluno["nome"])
      st.caption(aluno.get("objetivo") or "Objetivo não definido")
      if aluno.get("observacoes_medicas"):
        st.warning(aluno["observacoes_medicas"])
      for coluna, (texto, icone, pagina) in zip(st.columns(3), [
          ("Treinos", ":material/fitness_center:", "pages/02_Treinos.py"),
          ("Avaliações", ":material/monitoring:", "pages/03_Avaliacoes.py"),
          ("Financeiro", ":material/account_balance_wallet:", "pages/04_Financeiro.py"),
      ]):
        if coluna.button(texto, icon=icone, width="stretch"):
          if st.session_state.get("aluno_selecionado_id") != aluno["id"]:
            st.session_state.pop("itens_treino_temp", None)
          st.session_state.aluno_selecionado_id = aluno["id"]
          st.switch_page(pagina)
    else:
      st.info("Selecione um aluno na tabela para acessar Treinos, Avaliações e Financeiro.")
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
