import streamlit as st

from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.cards import metric_card
from interfaz.components.tables import curso_to_dict


def _cursos_docente(sistema, docente):
    if not docente:
        return []

    return [curso for curso in sistema.cursos.values() if curso.docente == docente]


def mostrar_dashboard_docente(sistema):
    encabezado_pagina("Panel del docente")

    docente = obtener_usuario_actual(sistema)

    if not docente:
        st.warning("No se encontro un docente seleccionado.")
        return

    st.markdown(f"### Bienvenido, {docente.nombres} {docente.apellidos}")
    st.caption("Vista academica de consulta para docentes.")

    cursos = _cursos_docente(sistema, docente)
    total_estudiantes = sum(len(curso.lista_estudiantes) for curso in cursos)

    col1, col2, col3 = st.columns(3)

    with col1:
        metric_card("Cursos asignados", len(cursos))

    with col2:
        metric_card("Estudiantes asignados", total_estudiantes)

    with col3:
        metric_card("Periodo", sistema.periodo_actual)

    st.divider()
    st.subheader("Mis cursos asignados")

    if not cursos:
        st.info("Este docente no tiene cursos asignados en el periodo actual.")
        return

    filas = [curso_to_dict(curso) for curso in cursos]
    st.dataframe(filas, use_container_width=True, hide_index=True)
