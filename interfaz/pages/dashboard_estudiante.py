import streamlit as st

from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.cards import metric_card
from interfaz.components.tables import carga_to_dict, curso_to_dict


def _cursos_estudiante(sistema, estudiante):
    if not estudiante:
        return []

    return sistema.obtener_cursos_estudiante(estudiante)


def _cargas_estudiante(sistema, estudiante):
    if not estudiante:
        return []

    return [
        carga
        for carga in sistema.cargas_academicas.values()
        if carga.estudiante == estudiante
    ]


def mostrar_dashboard_estudiante(sistema):
    encabezado_pagina("Panel del estudiante")

    estudiante = obtener_usuario_actual(sistema)

    if not estudiante:
        st.warning("No se encontro un estudiante seleccionado.")
        return

    st.markdown(f"### Bienvenido, {estudiante.nombres} {estudiante.apellidos}")
    st.caption("Vista personal de consulta academica para estudiantes.")

    cursos = _cursos_estudiante(sistema, estudiante)
    cargas = _cargas_estudiante(sistema, estudiante)

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Cursos inscritos", len(cursos))

    with col2:
        metric_card("Estado", estudiante.estado_nivelacion)

    with col3:
        metric_card("Periodo", sistema.periodo_actual)

    st.divider()
    st.subheader("Mis cursos")

    if cursos:
        filas = [curso_to_dict(curso) for curso in cursos]
        st.dataframe(filas, use_container_width=True, hide_index=True)
    else:
        st.info("Todavia no tienes cursos inscritos.")

    st.divider()
    st.subheader("Mi carga academica")

    if cargas:
        filas = [carga_to_dict(carga) for carga in cargas]
        st.dataframe(filas, use_container_width=True, hide_index=True)
    else:
        st.info("Todavia no tienes una carga academica generada.")
