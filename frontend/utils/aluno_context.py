"""Seleção por ID compartilhada entre os módulos de acompanhamento."""
import streamlit as st


def selecionar_aluno(alunos, label, key):
    por_id = {a["id"]: a for a in alunos}
    ids = list(por_id)
    atual = st.session_state.get("aluno_selecionado_id")
    # Sincroniza o widget ao abrir um módulo a partir da Gestão de Alunos.
    if st.session_state.get(key) != atual or atual not in por_id:
        st.session_state[key] = atual if atual in por_id else ids[0]
    def mudou():
        st.session_state.aluno_selecionado_id = st.session_state[key]
        st.session_state.pop("itens_treino_temp", None)

    escolhido = st.selectbox(
        label, options=ids, key=key,
        format_func=lambda ident: f"{por_id[ident]['nome']} · #{ident}",
        on_change=mudou,
    )
    if escolhido != atual:
        st.session_state.pop("itens_treino_temp", None)
    st.session_state.aluno_selecionado_id = escolhido
    return por_id[escolhido]
