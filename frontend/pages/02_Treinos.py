import streamlit as st
from services.api_client import (
    criar_exercicio,
    criar_ficha_treino,
    get_alunos,
    get_exercicios,
    get_fichas_aluno,
)

st.set_page_config(
    page_title="Gestão de Fichas e Treinos", page_icon="🏋️‍♂️", layout="wide"
)

st.title("🏋️‍♂️ Gestão de Treinos e Exercícios")

# Abas principais da tela
aba_construtor, aba_catalogo, aba_visualizar = st.tabs([
    "📋 Montar Ficha de Treino",
    "📚 Catálogo de Exercícios",
    "👁️ Visualizar Fichas do Aluno",
])

# ==========================================
# ABA 1: CONSTRUTOR DE FICHA DE TREINO
# ==========================================
with aba_construtor:
  st.subheader("Construtor de Fichas Personalizadas")

  alunos = get_alunos()
  exercicios = get_exercicios()

  if not alunos:
    st.warning("Cadastre pelo menos um aluno antes de montar uma ficha.")
  elif not exercicios:
    st.warning(
        "Cadastre exercícios na aba 'Catálogo de Exercícios' antes de montar a"
        " ficha."
    )
  else:
    # Seleção do Aluno
    aluno_dict = {a["nome"]: a["id"] for a in alunos}
    aluno_selecionado = st.selectbox(
        "Selecione o Aluno", options=list(aluno_dict.keys())
    )
    aluno_id = aluno_dict[aluno_selecionado]

    with st.form("form_ficha_treino"):
      titulo_ficha = st.text_input(
          "Título da Ficha (Ex: Hipertrofia - Fase 1 ABC)"
      )
      descricao_ficha = st.text_area(
          "Observações gerais do treino (Opcional)"
      )

      st.markdown("---")
      st.markdown("### 📝 Adicionar Exercícios à Ficha")

      # Gerenciamento de itens de treino dinâmicos no Streamlit Session State
      if "itens_treino_temp" not in st.session_state:
        st.session_state.itens_treino_temp = []

      # Formulário interno para adicionar exercício na lista temporária
      col1, col2, col3 = st.columns(3)
      with col1:
        exercicio_dict = {e["nome"]: e["id"] for e in exercicios}
        ex_nome = st.selectbox(
            "Exercício", options=list(exercicio_dict.keys()), key="temp_ex"
        )
      with col2:
        divisao = st.selectbox(
            "Divisão", options=["A", "B", "C", "D", "E", "Fullbody"], key="temp_div"
        )
      with col3:
        series = st.number_input(
            "Séries", min_value=1, max_value=10, value=3, key="temp_ser"
        )

      col4, col5, col6 = st.columns(3)
      with col4:
        repeticoes = st.text_input(
            "Repetições (Ex: 10-12)", value="10-12", key="temp_rep"
        )
      with col5:
        carga = st.number_input(
            "Carga Inicial (kg)", min_value=0.0, value=0.0, key="temp_carga"
        )
      with col6:
        descanso = st.number_input(
            "Descanso (segundos)", min_value=10, value=60, step=10, key="temp_desc"
        )

      obs_item = st.text_input(
          "Observação do Exercício (Ex: Bi-set, Cadência 3010)", key="temp_obs"
      )

      btn_add = st.form_submit_button("➕ Adicionar Exercício à Ficha")

      if btn_add:
        novo_item = {
            "exercicio_id": exercicio_dict[ex_nome],
            "exercicio_nome": ex_nome,
            "divisao": divisao,
            "series": series,
            "repeticoes": repeticoes,
            "carga_kg": carga,
            "descanso_segundos": descanso,
            "ordem": len(st.session_state.itens_treino_temp) + 1,
            "observacoes": obs_item,
        }
        st.session_state.itens_treino_temp.append(novo_item)
        st.success(f"Exercício '{ex_nome}' adicionado com sucesso!")

      # Exibe lista temporária de exercícios adicionados
      if st.session_state.itens_treino_temp:
        st.markdown("#### 📋 Exercícios na Ficha Atual:")
        for idx, item in enumerate(st.session_state.itens_treino_temp):
          st.write(
              f"**{idx+1}. [{item['divisao']}] {item['exercicio_nome']}**"
              f" — {item['series']}x{item['repeticoes']} | Carga:"
              f" {item['carga_kg']}kg | Descanso: {item['descanso_segundos']}s"
          )

        if st.button("🗑️ Limpar Lista de Exercícios"):
          st.session_state.itens_treino_temp = []
          st.rerun()

      # Botão para salvar a ficha completa no Backend
      salvar_ficha = st.button("💾 Salvar e Publicar Ficha de Treino")

      if salvar_ficha:
        if not titulo_ficha:
          st.error("Informe o título da ficha de treino.")
        elif not st.session_state.itens_treino_temp:
          st.error("Adicione pelo menos um exercício à ficha.")
        else:
          payload = {
              "aluno_id": aluno_id,
              "titulo": titulo_ficha,
              "descricao": descricao_ficha,
              "itens": [
                  {
                      k: v
                      for k, v in item.items()
                      if k != "exercicio_nome"  # Remove campo auxiliar
                  }
                  for item in st.session_state.itens_treino_temp
              ],
          }
          response = criar_ficha_treino(payload)
          if response and response.status_code == 201:
            st.success("Ficha de treino criada com sucesso!")
            st.session_state.itens_treino_temp = []
          else:
            st.error("Erro ao salvar a ficha. Verifique a conexão com a API.")

# ==========================================
# ABA 2: CATÁLOGO DE EXERCÍCIOS
# ==========================================
with aba_catalogo:
  st.subheader("Biblioteca de Exercícios")

  col_cad, col_list = st.columns([1, 1])

  with col_cad:
    st.markdown("#### Cadastrar Novo Exercício")
    with st.form("form_cad_exercicio"):
      nome_ex = st.text_input("Nome do Exercício * (Ex: Supino Reto)")
      grupo_musc = st.selectbox(
          "Grupo Muscular *",
          options=[
              "Peitoral",
              "Dorsal / Costas",
              "Quadríceps",
              "Posterior de Coxa",
              "Glúteos",
              "Ombros",
              "Bíceps",
              "Tríceps",
              "Abdominais",
              "Panturrilhas",
              "Cardio",
          ],
      )
      url_vid = st.text_input(
          "Link de Vídeo Demonstrativo (YouTube / URL Opcional)"
      )

      submitted_ex = st.form_submit_button("Salvar Exercício")

      if submitted_ex:
        if not nome_ex:
          st.error("O nome do exercício é obrigatório.")
        else:
          payload_ex = {
              "nome": nome_ex,
              "grupo_muscular": grupo_musc,
              "url_video": url_vid,
          }
          res = criar_exercicio(payload_ex)
          if res and res.status_code == 201:
            st.success(f"Exercício '{nome_ex}' cadastrado com sucesso!")
            st.rerun()
          else:
            st.error("Erro ao cadastrar exercício.")

  with col_list:
    st.markdown("#### Exercícios Disponíveis no Sistema")
    exercicios_cadastrados = get_exercicios()
    if exercicios_cadastrados:
      for ex in exercicios_cadastrados:
        st.write(
            f"💪 **{ex['nome']}** — *{ex['grupo_muscular']}*"
            + (f" [🔗 Vídeo]({ex['url_video']})" if ex["url_video"] else "")
        )
    else:
      st.info("Nenhum exercício cadastrado no catálogo.")

# ==========================================
# ABA 3: VISUALIZAR FICHAS DO ALUNO
# ==========================================
with aba_visualizar:
  st.subheader("Histórico de Fichas Prescritas")
  if alunos:
    aluno_dict_viz = {a["nome"]: a["id"] for a in alunos}
    aluno_sel_viz = st.selectbox(
        "Selecione o Aluno para Auditoria",
        options=list(aluno_dict_viz.keys()),
        key="viz_aluno",
    )
    id_aluno_viz = aluno_dict_viz[aluno_sel_viz]

    fichas = get_fichas_aluno(id_aluno_viz)
    if fichas:
      for ficha in fichas:
        with st.expander(
            f"📄 {ficha['titulo']} (Ativa: {'Sim' if ficha['ativa'] else 'Não'})"
        ):
          st.write(f"**Descrição:** {ficha.get('descricao', 'Nenhuma')}")
          st.markdown("---")
          for item in ficha.get("itens", []):
            ex_info = item.get("exercicio", {})
            st.write(
                f"• **[{item['divisao']}] {ex_info.get('nome', 'Exercício')}**"
                f" — {item['series']} séries de {item['repeticoes']} reps |"
                f" Carga: {item['carga_kg']}kg | Descanso:"
                f" {item['descanso_segundos']}s"
            )
            if item.get("observacoes"):
              st.caption(f"Obs: {item['observacoes']}")
    else:
      st.info("Este aluno ainda não possui fichas de treino cadastradas.")
  else:
    st.warning("Nenhum aluno cadastrado.")