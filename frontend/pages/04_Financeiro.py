from datetime import date
import pandas as pd
import streamlit as st
from utils.aluno_context import selecionar_aluno
from services.demo import mostrar_aviso
from services.api_client import (
    atualizar_mensalidade,
    criar_mensalidade,
    get_alunos,
    get_mensalidades_aluno,
)

st.set_page_config(
    initial_sidebar_state="auto",
    page_title="Gestão Financeira", page_icon=":material/account_balance_wallet:", layout="wide"
)

st.title("Gestão Financeira de Mensalidades", icon=":material/account_balance_wallet:")
mostrar_aviso()

alunos = get_alunos()

if not alunos:
  st.warning("Cadastre alunos para gerenciar as mensalidades.")
else:
  aluno = selecionar_aluno(alunos, "Selecione o Aluno", "financeiro_aluno")
  aluno_sel, aluno_id = aluno["nome"], aluno["id"]

  aba_consulta, aba_nova = st.tabs(
      [":material/receipt_long: Mensalidades do Aluno", ":material/add_card: Lançar Nova Mensalidade"]
  )

  with aba_consulta:
    st.subheader(f"Histórico Financeiro - {aluno_sel}")
    mensalidades = get_mensalidades_aluno(aluno_id)

    if mensalidades:
      for m in mensalidades:
        col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
        col1.write(f"**Vencimento:** {m['data_vencimento']}")
        col2.write(f"**Valor:** R$ {m['valor']:.2f}")

        # Cor do Status
        status_color = "🟢" if m["status"] == "PAGO" else "🔴"
        col3.write(f"**Status:** {status_color} {m['status']}")

        # Botão para dar baixa no pagamento
        if m["status"] != "PAGO":
          if col4.button("✅ Dar Baixa (Pago)", key=f"btn_{m['id']}"):
            res = atualizar_mensalidade(m["id"], {"status": "PAGO"})
            if res and res.status_code == 200:
              st.success("Pagamento registrado!")
              st.rerun()
            else:
              st.error("Erro ao dar baixa.")
        else:
          col4.write(f"Pago em: {m.get('data_pagamento', 'N/I')}")
        st.markdown("---")
    else:
      st.info("Nenhuma mensalidade lançada para este aluno.")

  with aba_nova:
    st.subheader("Gerar Cobrança de Mensalidade")
    with st.form("form_mensalidade"):
      col_venc, col_val = st.columns(2)
      data_venc = col_venc.date_input("Data de Vencimento", value=date.today())
      valor = col_val.number_input(
          "Valor (R$)", min_value=1.0, value=150.0, step=10.0
      )

      submit = st.form_submit_button("💾 Gerar Mensalidade")

      if submit:
        payload = {
            "aluno_id": aluno_id,
            "data_vencimento": str(data_venc),
            "valor": valor,
            "status": "PENDENTE",
        }
        res = criar_mensalidade(payload)
        if res and res.status_code == 201:
          st.success("Mensalidade gerada com sucesso!")
          st.rerun()
        else:
          st.error("Erro ao gerar mensalidade.")
