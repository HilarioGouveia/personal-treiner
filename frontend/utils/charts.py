"""Gráficos de evolução com marcadores visíveis desde a primeira avaliação."""

import altair as alt


def grafico_evolucao(df, campo, rotulo):
    dados = df[["data_avaliacao", campo]].dropna().sort_values("data_avaliacao")
    return (
        alt.Chart(dados)
        .mark_line(point=alt.OverlayMarkDef(filled=True, size=80))
        .encode(
            x=alt.X("data_avaliacao:T", title="Data", axis=alt.Axis(format="%d/%m/%Y", tickCount=3)),
            y=alt.Y(f"{campo}:Q", title=rotulo),
            tooltip=[
                alt.Tooltip("data_avaliacao:T", title="Data", format="%d/%m/%Y"),
                alt.Tooltip(f"{campo}:Q", title=rotulo, format=".1f"),
            ],
        )
        .properties(height=260)
    )
