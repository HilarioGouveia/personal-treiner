from datetime import date
import pandas as pd
import streamlit as st
from services.api_client import (
    criar_avaliacao,
    get_alunos,
    get_avaliacoes_aluno,
)

st.set_page_config(
    page_title="Avaliação Física e Evolução", page_icon="📈", layout="wide"
)

st.title("📈 Avaliação Física e Gráficos de Evolução")

alunos = get_alunos()

if not alunos:
  st.warning("Cadastre pelo menos um aluno para gerenciar avaliações físicas.")
else:
  aluno_dict = {a["nome"]: a["id"] for a in alunos}
  aluno_selecionado = st.selectbox(
      "Selecione o Aluno", options=list(aluno_dict.keys())
  )
  aluno_id = aluno_dict[aluno_selecionado]

  aba_graficos, aba_registro = st.tabs([
      "📉 Evolução e Gráficos",
      "➕ Nova Avaliação Física",
  ])

  # ==========================================
  # ABA 1: GRÁFICOS DE EVOLUÇÃO
  # ==========================================
  with aba_graficos:
    st.subheader(f"Histórico de Evolução de {aluno_selecionado}")
    avaliacoes = get_avaliacoes_aluno(aluno_id)

    if avaliacoes:
      # Converte o histórico em DataFrame Pandas para facilitar a plotagem
      df = pd.DataFrame(avaliacoes)
      df["data_avaliacao"] = pd.to_datetime(df["data_avaliacao"])
      df = df.sort_values("data_avaliacao")

      # Métricas resumidas (Cards)
      col1, col2, col3 = st.columns(3)
      with col1:
        peso_atual = df["peso_kg"].iloc[-1]
        peso_inicial = df["peso_kg"].iloc[0]
        delta_peso = peso_atual - peso_inicial
        st.metric(
            "Peso Atual",
            f"{peso_atual} kg",
            delta=f"{delta_peso:.1f} kg" if len(df) > 1 else None,
        )
      with col2:
        if "percentual_gordura" in df.columns and df["percentual_gordura"].notna().any():
          gordura_atual = df["percentual_gordura"].iloc[-1]
          st.metric("% de Gordura Atual", f"{gordura_atual}%")
        else:
          st.metric("% de Gordura Atual", "Não informado")
      with col3:
        st.metric("Total de Avaliações", len(df))

      st.markdown("---")
      st.markdown("### 📊 Gráfico de Evolução de Peso (kg)")
      # Prepara dataframe para o gráfico de linha do Streamlit
      df_peso = df.set_index("data_avaliacao")[["peso_kg"]]
      st.line_chart(df_peso)

      if "percentual_gordura" in df.columns and df["percentual_gordura"].notna().any():
        st.markdown("### 📊 Gráfico de Evolução de % de Gordura")
        df_gordura = df.set_index("data_avaliacao")[["percentual_gordura"]]
        st.line_chart(df_gordura)

      st.markdown("---")
      st.markdown("### 📋 Tabela Detalhada de Registros")
      st.dataframe(df[["data_avaliacao", "peso_kg", "altura_cm", "percentual_gordura", "observacoes"]])

    else:
      st.info("Nenhuma avaliação física registrada para este aluno.")

  # ==========================================
  # ABA 2: REGISTRO DE NOVA AVALIAÇÃO
  # ==========================================
  with aba_registro:
    st.subheader("Registrar Nova Avaliação Antropométrica")

    with st.form("form_avaliacao"):
      col1, col2, col3 = st.columns(3)
      with col1:
        data_av = st.date_input("Data da Avaliação", value=date.today())
        peso = st.number_input(
            "Peso (kg) *", min_value=20.0, max_value=300.0, value=70.0, step=0.1
        )
      with col2:
        altura = st.number_input(
            "Altura (cm)", min_value=100.0, max_value=250.0, value=175.0, step=1.0
        )
        gordura = st.number_input(
            "% de Gordura (Opcional)",
            min_value=1.0,
            max_value=60.0,
            value=15.0,
            step=0.1,
        )
      with col3:
        st.markdown("**Perímetros / Dobras (Opcional)**")
        braco = st.number_input("Braço (cm)", value=0.0)
        cintura = st.number_input("Cintura (cm)", value=0.0)

      obs = st.text_area(
          "Observações da Avaliação (Ex: Condições de medição, feedback)"
      )

      submitted_av = st.form_submit_button("💾 Salvar Avaliação Física")

      if submitted_av:
        medidas_dict = {}
        if braco > 0:
          medidas_dict["braco_cm"] = braco
        if cintura > 0:
          medidas_dict["cintura_cm"] = cintura

        payload_av = {
            "aluno_id": aluno_id,
            "data_avaliacao": str(data_av),
            "peso_kg": peso,
            "altura_cm": altura if altura > 0 else None,
            "percentual_gordura": gordura if gordura > 0 else None,
            "medidas_json": medidas_dict if medidas_dict else None,
            "observacoes": obs,
        }

        res = criar_avaliacao(payload_av)
        if res and res.status_code == 201:
          st.success("Avaliação física registrada com sucesso!")
          st.rerun()
        else:
          st.error(
              "Erro ao registrar avaliação. Verifique a conexão com a API."
          )