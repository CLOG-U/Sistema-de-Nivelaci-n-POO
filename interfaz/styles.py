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


def aplicar_estilos_login():
    st.markdown(
        f"""
        <style>
            section[data-testid="stSidebar"] {{
                display: none !important;
            }}
            .main .block-container {{
                max-width: 100% !important;
                padding-top: 0 !important;
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }}
            [data-testid="stAppViewContainer"] {{
                background-color: #ececec !important;
            }}
            .main {{
                background-color: #ececec !important;
            }}
            .uleam-topbar {{
                background: linear-gradient(90deg, {COLOR_NEGRO} 0%, {COLOR_NEGRO_SUAVE} 100%);
                border-bottom: 3px solid {COLOR_ROJO};
                padding: 10px 24px;
                margin: -1rem -1rem 2rem -1rem;
            }}
            .uleam-topbar-inner {{
                display: flex;
                align-items: center;
                justify-content: space-between;
                max-width: 1100px;
                margin: 0 auto;
            }}
            .uleam-topbar-logo-img {{
                height: 42px;
                background: {COLOR_BLANCO};
                padding: 4px 8px;
                border-radius: 4px;
            }}
            .uleam-topbar-siglas {{
                color: {COLOR_VERDE};
                font-size: 1.4rem;
                font-weight: 700;
            }}
            .uleam-topbar-actions {{
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            .uleam-lang {{
                color: {COLOR_BLANCO};
                font-size: 0.85rem;
                font-weight: 600;
            }}
            .uleam-lang-muted {{
                opacity: 0.55;
            }}
            .uleam-lang-sep {{
                color: #888;
            }}
            .login-card {{
                background: {COLOR_BLANCO};
                border: 1px solid #d9d9d9;
                border-radius: 10px;
                padding: 28px 32px 20px 32px;
                box-shadow: 0 8px 24px rgba(0,0,0,0.08);
                margin-top: 1rem;
            }}
            .login-card-header {{
                text-align: center;
                margin-bottom: 8px;
            }}
            .login-title {{
                color: {COLOR_NEGRO};
                font-size: 1.15rem;
                font-weight: 700;
                margin: 8px 0 4px 0;
                border: none;
                padding: 0;
            }}
            .login-subtitle {{
                color: {COLOR_GRIS_OSCURO};
                font-size: 0.82rem;
                margin: 0 0 16px 0;
            }}
            [data-testid="stForm"] {{
                border: none !important;
                box-shadow: none !important;
                padding: 0 !important;
                background: transparent !important;
            }}
            [data-testid="stForm"] label {{
                color: {COLOR_GRIS_OSCURO} !important;
                font-weight: 600 !important;
            }}
            [data-testid="stFormSubmitButton"] button {{
                background-color: {COLOR_ROJO} !important;
                color: {COLOR_BLANCO} !important;
                border: none !important;
                font-weight: 600 !important;
                padding: 0.55rem 1rem !important;
            }}
            [data-testid="stFormSubmitButton"] button:hover {{
                background-color: {COLOR_NEGRO} !important;
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
