"""Dados fictícios independentes para cada sessão de demonstração."""

import os
from copy import deepcopy
from datetime import date, timedelta

import streamlit as st
from requests import Response


def ativo():
    value = os.getenv("DEMO_MODE")
    if value is None:
        try:
            value = st.secrets.get("DEMO_MODE", False)
        except FileNotFoundError:
            value = False
    return str(value).strip().lower() in {"true", "1", "yes"}


def exemplos():
    hoje = date.today()
    alunos = [
        dict(id=1, usuario_id=1, nome="Ana Exemplo", email="ana@example.com", telefone="(11) 90000-0001", data_nascimento="1992-05-14", objetivo="Hipertrofia", observacoes_medicas="Dados fictícios para demonstração."),
        dict(id=2, usuario_id=2, nome="Bruno Exemplo", email="bruno@example.com", telefone="(11) 90000-0002", data_nascimento="1988-09-22", objetivo="Condicionamento", observacoes_medicas="Dados fictícios para demonstração."),
    ]
    exercicios = [
        dict(id=1, nome="Supino reto", grupo_muscular="Peitoral", url_video=None),
        dict(id=2, nome="Agachamento", grupo_muscular="Quadríceps", url_video=None),
        dict(id=3, nome="Remada baixa", grupo_muscular="Dorsal / Costas", url_video=None),
    ]
    avaliacoes = []
    for aluno in alunos:
        for i in range(4):
            avaliacoes.append(dict(id=len(avaliacoes)+1, aluno_id=aluno["id"], data_avaliacao=(hoje-timedelta(days=(3-i)*30)).isoformat(), peso_kg=78-i*0.8+aluno["id"], altura_cm=175, percentual_gordura=22-i, medidas_json={"braco_cm": 32+i*0.3}, observacoes="Avaliação fictícia de acompanhamento."))
    itens = [dict(id=1, exercicio_id=1, exercicio=deepcopy(exercicios[0]), divisao="A", series=3, repeticoes="10-12", carga_kg=20, descanso_segundos=60, ordem=1, observacoes="Execução controlada.")]
    return dict(alunos=alunos, exercicios=exercicios, avaliacoes=avaliacoes,
                fichas=[dict(id=1, aluno_id=1, titulo="Hipertrofia — Fase 1", descricao="Ficha fictícia para apresentação", ativa=True, itens=itens)],
                mensalidades=[dict(id=1, aluno_id=1, data_vencimento=(hoje-timedelta(days=5)).isoformat(), valor=180, status="PAGO", data_pagamento=(hoje-timedelta(days=6)).isoformat()),
                              dict(id=2, aluno_id=1, data_vencimento=(hoje+timedelta(days=25)).isoformat(), valor=180, status="PENDENTE", data_pagamento=None),
                              dict(id=3, aluno_id=2, data_vencimento=(hoje-timedelta(days=10)).isoformat(), valor=150, status="ATRASADO", data_pagamento=None)])


def banco():
    if "demo_dados" not in st.session_state:
        st.session_state.demo_dados = exemplos()
    return st.session_state.demo_dados


def resposta(status, dados):
    import json
    response = Response()
    response.status_code = status
    response.encoding = "utf-8"
    response._content = json.dumps(dados, ensure_ascii=False).encode("utf-8")
    response.headers["Content-Type"] = "application/json"
    return response


def listar(tabela, aluno_id=None):
    rows = banco()[tabela]
    if aluno_id is not None:
        rows = [row for row in rows if row["aluno_id"] == aluno_id]
    if tabela == "avaliacoes":
        rows = sorted(rows, key=lambda row: row["data_avaliacao"])
    elif tabela == "mensalidades":
        rows = sorted(rows, key=lambda row: row["data_vencimento"], reverse=True)
    return deepcopy(rows)


def criar(tabela, dados):
    db = banco()
    row = deepcopy(dados)
    row.pop("senha", None)
    if tabela == "alunos" and any(a["email"].lower() == row["email"].lower() for a in db["alunos"]):
        return resposta(400, {"detail": "E-mail já cadastrado no sistema."})
    if tabela in {"fichas", "avaliacoes", "mensalidades"} and not any(a["id"] == row["aluno_id"] for a in db["alunos"]):
        return resposta(404, {"detail": "Aluno não encontrado."})
    row["id"] = max((item["id"] for item in db[tabela]), default=0) + 1
    if tabela == "alunos":
        row["usuario_id"] = row["id"]
    elif tabela == "fichas":
        row["ativa"] = True
        for i, item in enumerate(row["itens"], 1):
            exercicio = next((e for e in db["exercicios"] if e["id"] == item["exercicio_id"]), None)
            if exercicio is None:
                return resposta(404, {"detail": "Exercício não encontrado."})
            item.update(id=i, exercicio=deepcopy(exercicio))
    elif tabela == "avaliacoes":
        row["data_avaliacao"] = row.get("data_avaliacao") or date.today().isoformat()
    elif tabela == "mensalidades":
        row.setdefault("status", "PENDENTE")
        row.setdefault("data_pagamento", None)
    db[tabela].append(row)
    return resposta(201, deepcopy(row))


def atualizar_mensalidade(identificador, dados):
    row = next((m for m in banco()["mensalidades"] if m["id"] == identificador), None)
    if row is None:
        return resposta(404, {"detail": "Mensalidade não encontrada."})
    row.update(deepcopy(dados))
    if row["status"] == "PAGO":
        row["data_pagamento"] = dados.get("data_pagamento") or date.today().isoformat()
    return resposta(200, deepcopy(row))


def mostrar_aviso():
    if not ativo():
        return
    st.sidebar.info("Modo demonstração · Dados fictícios. Alterações ficam apenas nesta sessão.")
    if st.sidebar.button("Restaurar demonstração", key="restaurar_demo"):
        st.session_state.demo_dados = exemplos()
        st.session_state.pop("itens_treino_temp", None)
        st.rerun()
