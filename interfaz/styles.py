import streamlit as st

from interfaz.branding import (
    COLOR_BLANCO,
    COLOR_GRIS_OSCURO,
    COLOR_NEGRO,
    COLOR_NEGRO_SUAVE,
    COLOR_ROJO,
    COLOR_VERDE,
    FACULTAD,
    SIGLAS,
    UNIVERSIDAD,
)


def aplicar_estilos():
    st.markdown(
        f"""
        <style>
            .main {{
                background-color: #f8f8f8;
            }}
            .main .block-container {{
                color: {COLOR_NEGRO};
            }}
            .main h1, .main h2, .main h3, .main h4 {{
                color: {COLOR_NEGRO} !important;
            }}
            [data-testid="stCaptionContainer"] p,
            [data-testid="stCaptionContainer"] {{
                color: {COLOR_GRIS_OSCURO} !important;
            }}
            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, {COLOR_NEGRO} 0%, {COLOR_NEGRO_SUAVE} 100%);
                border-right: 3px solid {COLOR_ROJO};
            }}
            [data-testid="stSidebarNav"] {{
                display: none !important;
            }}
            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] span,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] .stMarkdown,
            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
                color: {COLOR_BLANCO} !important;
            }}
            [data-testid="stSidebar"] .stSelectbox label {{
                color: #e8e8e8 !important;
            }}
            [data-testid="stSidebar"] [data-baseweb="select"] {{
                background-color: {COLOR_NEGRO_SUAVE} !important;
            }}
            [data-testid="stSidebar"] [data-baseweb="select"] * {{
                color: {COLOR_BLANCO} !important;
            }}
            [data-testid="stSidebar"] .stRadio label {{
                color: {COLOR_BLANCO} !important;
            }}
            [data-testid="stSidebar"] .stRadio label:hover {{
                color: {COLOR_VERDE} !important;
            }}
            [data-testid="stSidebar"] [data-testid="stAlert"] {{
                color: {COLOR_NEGRO} !important;
            }}
            [data-testid="stSidebar"] [data-testid="stAlert"] * {{
                color: {COLOR_NEGRO} !important;
            }}
            [data-testid="stMetric"] {{
                background-color: {COLOR_BLANCO};
                border-left: 4px solid {COLOR_VERDE};
                border-bottom: 2px solid {COLOR_ROJO};
                border-radius: 8px;
                padding: 12px;
                box-shadow: 0 2px 6px rgba(26, 26, 26, 0.1);
            }}
            [data-testid="stMetric"] label {{
                color: {COLOR_GRIS_OSCURO} !important;
            }}
            [data-testid="stMetric"] [data-testid="stMetricValue"] {{
                color: {COLOR_NEGRO} !important;
            }}
            [data-testid="stForm"] {{
                background-color: {COLOR_BLANCO};
                border: 1px solid #dddddd;
                border-top: 3px solid {COLOR_ROJO};
                border-radius: 10px;
                padding: 16px;
                box-shadow: 0 1px 4px rgba(26, 26, 26, 0.08);
            }}
            h1 {{
                color: {COLOR_NEGRO};
                border-left: 5px solid {COLOR_VERDE};
                padding-left: 10px;
            }}
            h2, h3 {{
                color: {COLOR_NEGRO_SUAVE};
            }}
            [data-testid="stCaptionContainer"] {{
                color: {COLOR_GRIS_OSCURO};
            }}
            .stButton > button {{
                background-color: {COLOR_ROJO};
                color: {COLOR_BLANCO};
                border: none;
            }}
            .stButton > button:hover {{
                background-color: {COLOR_NEGRO};
                color: {COLOR_BLANCO};
            }}
            .role-icon-wrap {{
                display: flex;
                align-items: center;
                justify-content: center;
                min-height: 90px;
                padding: 8px 4px;
            }}
            .role-icon {{
                font-size: 4rem;
                line-height: 1;
                display: block;
            }}
            .role-desc {{
                color: {COLOR_GRIS_OSCURO};
                font-size: 1rem;
                line-height: 1.5;
                margin: 0;
            }}
            div[data-testid="stVerticalBlockBorderWrapper"] {{
                border-top: 4px solid {COLOR_ROJO} !important;
                background: {COLOR_BLANCO};
                padding: 4px 0;
            }}
            .role-badge {{
                display:inline-block;
                padding:6px 12px;
                border-radius:999px;
                font-weight:600;
                font-size:0.85rem;
                background:{COLOR_NEGRO};
                color:{COLOR_BLANCO};
                margin-bottom:8px;
            }}
            .role-card {{
                background:{COLOR_BLANCO} !important;
                border:1px solid #dddddd;
                border-top:4px solid {COLOR_ROJO};
                border-radius:12px;
                padding:18px;
                box-shadow:0 2px 8px rgba(26,26,26,0.08);
                margin-bottom:14px;
            }}
            .role-card h2 {{
                color:{COLOR_NEGRO} !important;
                margin-bottom:4px;
            }}
            .role-card p {{
                color:{COLOR_GRIS_OSCURO} !important;
                font-size:0.95rem;
            }}
            .readonly-box {{
                background:#f7f7f7 !important;
                border-left:4px solid {COLOR_VERDE};
                padding:12px 14px;
                border-radius:8px;
                margin-bottom:12px;
                color:{COLOR_NEGRO_SUAVE} !important;
            }}
            .login-card {{
                background:{COLOR_BLANCO};
                border:1px solid #dddddd;
                border-top:4px solid {COLOR_ROJO};
                border-radius:12px;
                padding:24px 20px;
                box-shadow:0 4px 12px rgba(26,26,26,0.1);
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def pie_pagina():
    st.markdown(
        f'<hr style="border:none;border-top:2px solid {COLOR_VERDE};margin-top:24px;">',
        unsafe_allow_html=True,
    )
    st.caption(f"{SIGLAS} · {UNIVERSIDAD} · {FACULTAD}")
