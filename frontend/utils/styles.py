import streamlit as st


def aplicar_estilo_tech_minimalista():
  st.html(
      """
        <style>
            /* Importar fonte geométrica moderna */
            @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap');

            /* Aplicar fonte global */
            html, body, [class*="css"] {
                font-family: 'Plus Jakarta Sans', sans-serif;
            }

            /* Métricas e números com estilo Tech (Monoespaçado) */
            [data-testid="stMetricValue"], .tech-number {
                font-family: 'JetBrains Mono', monospace !important;
                color: #00E5FF !important;
                letter-spacing: -0.5px;
            }

            /* Estilização de Cartões (Glassmorphism Minimalista) */
            div.stMetric, div[data-testid="stVerticalBlock"] > div.element-container > div.stMarkdown {
                background-color: #161B22;
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 1rem;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
            }

            /* Botões de Ação com Efeito Tech Glow */
            .stButton > button {
                background: linear-gradient(135deg, #00E5FF 0%, #0088CC 100%);
                color: #0E1117;
                font-weight: 700;
                border: none;
                border-radius: 8px;
                padding: 0.5rem 1rem;
                transition: all 0.3s ease;
                box-shadow: 0 0 15px rgba(0, 229, 255, 0.2);
            }

            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 0 25px rgba(0, 229, 255, 0.4);
                background: linear-gradient(135deg, #33EDFF 0%, #0099DD 100%);
            }

            /* Separadores subtis */
            hr {
                border-color: rgba(255, 255, 255, 0.08);
            }
        </style>
        """,
  )
