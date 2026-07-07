"""Textos e identidad institucional ULEAM."""

UNIVERSIDAD = "Universidad Laica Eloy Alfaro de Manabi"
SIGLAS = "ULEAM"
NOMBRE_SISTEMA = "Sistema de Nivelacion Academica"
MODULO_POO = "Programacion Orientada a Objetos"
FACULTAD = "Facultad de Ingenieria Informatica y Ciencias Computacionales"
PERIODO_ACTUAL = "2026-1"
TITULO_APP = f"{SIGLAS} | {NOMBRE_SISTEMA}"


def encabezado_sidebar():
    return f"""
    <div style="text-align:center;padding-bottom:8px;">
        <p style="color:#7CFC00;font-size:1.4rem;font-weight:bold;margin:0;">{SIGLAS}</p>
        <p style="color:#ffffff;font-size:0.78rem;margin:4px 0 0 0;line-height:1.3;">{UNIVERSIDAD}</p>
        <p style="color:#dbeafe;font-size:0.75rem;margin:6px 0 0 0;">{NOMBRE_SISTEMA}</p>
        <p style="color:#dbeafe;font-size:0.72rem;margin:2px 0 0 0;">{MODULO_POO}</p>
    </div>
    """


def encabezado_pagina(titulo_modulo):
    import streamlit as st

    st.markdown(
        f"""
        <div style="margin-bottom:12px;">
            <span style="color:#00843D;font-weight:bold;font-size:1rem;">{SIGLAS}</span>
            <span style="color:#004B87;font-size:0.95rem;"> · {UNIVERSIDAD}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption(f"{NOMBRE_SISTEMA} · {MODULO_POO} · Periodo {PERIODO_ACTUAL}")
    st.title(titulo_modulo)
