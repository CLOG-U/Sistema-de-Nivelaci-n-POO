"""Textos e identidad institucional ULEAM."""

UNIVERSIDAD = "Universidad Laica Eloy Alfaro de Manabi"
SIGLAS = "ULEAM"
NOMBRE_SISTEMA = "Sistema de Nivelacion Academica"
MODULO_POO = "Programacion Orientada a Objetos"
FACULTAD = "Facultad de Ingenieria Informatica y Ciencias Computacionales"
PERIODO_ACTUAL = "2026-1"
TITULO_APP = f"{SIGLAS} | {NOMBRE_SISTEMA}"

# Paleta: rojo, blanco, verde y tonos negros
COLOR_ROJO = "#CE1126"
COLOR_VERDE = "#009639"
COLOR_BLANCO = "#FFFFFF"
COLOR_NEGRO = "#1A1A1A"
COLOR_NEGRO_SUAVE = "#2D2D2D"
COLOR_GRIS_OSCURO = "#404040"


def encabezado_sidebar():
    return f"""
    <div style="text-align:center;padding-bottom:8px;">
        <p style="color:{COLOR_VERDE};font-size:1.4rem;font-weight:bold;margin:0;">{SIGLAS}</p>
        <p style="color:{COLOR_BLANCO};font-size:0.78rem;margin:4px 0 0 0;line-height:1.3;">{UNIVERSIDAD}</p>
        <p style="color:#f0f0f0;font-size:0.75rem;margin:6px 0 0 0;">{NOMBRE_SISTEMA}</p>
        <p style="color:#e0e0e0;font-size:0.72rem;margin:2px 0 0 0;">{MODULO_POO}</p>
        <div style="height:3px;background:linear-gradient(90deg,{COLOR_ROJO},{COLOR_BLANCO},{COLOR_VERDE});
                    margin-top:10px;border-radius:2px;"></div>
    </div>
    """


def encabezado_pagina(titulo_modulo, periodo=None):
    import streamlit as st

    periodo_texto = periodo or PERIODO_ACTUAL
    st.markdown(
        f"""
        <div style="margin-bottom:12px;padding-bottom:8px;border-bottom:2px solid {COLOR_ROJO};">
            <span style="color:{COLOR_VERDE};font-weight:bold;font-size:1rem;">{SIGLAS}</span>
            <span style="color:{COLOR_NEGRO};font-size:0.95rem;"> · {UNIVERSIDAD}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(f"{NOMBRE_SISTEMA} · {MODULO_POO} · Periodo {periodo_texto}")
    st.title(titulo_modulo)
