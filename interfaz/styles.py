import streamlit as st

from interfaz.branding import FACULTAD, SIGLAS, UNIVERSIDAD


def aplicar_estilos():
    st.markdown(
        """
        <style>
            .main {
                background-color: #f4f7fb;
            }
            [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #004B87 0%, #003366 100%);
            }
            [data-testid="stSidebar"] .stRadio label {
                color: #ffffff !important;
            }
            [data-testid="stMetric"] {
                background-color: #ffffff;
                border-left: 4px solid #00843D;
                border-radius: 8px;
                padding: 12px;
                box-shadow: 0 1px 3px rgba(0, 75, 135, 0.08);
            }
            [data-testid="stForm"] {
                background-color: #ffffff;
                border: 1px solid #c5d7eb;
                border-top: 3px solid #004B87;
                border-radius: 10px;
                padding: 16px;
            }
            h1 {
                color: #004B87;
            }
            h2, h3 {
                color: #003366;
            }
            [data-testid="stCaptionContainer"] {
                color: #4b5563;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def pie_pagina():
    st.markdown("---")
    st.caption(f"{SIGLAS} · {UNIVERSIDAD} · {FACULTAD}")
