import streamlit as st

from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.cards import metric_card
from interfaz.components.layout import fila_metricas, intro_modulo, tabla_o_vacio
from interfaz.components.tables import calificacion_registro_to_dict, curso_to_dict


def _cursos_docente(sistema, docente):
    if not docente:
        return []
    return [curso for curso in sistema.cursos.values() if curso.docente == docente]


def _resumen_docente(sistema, docente):
    intro_modulo("Resumen academico del docente en el periodo activo.", "👨‍🏫")
    cursos = _cursos_docente(sistema, docente)
    total_estudiantes = sum(len(curso.lista_estudiantes) for curso in cursos)
    calificaciones = [
        registro
        for registro in sistema.calificaciones.values()
        if registro["docente"] == docente
    ]
    asistencias = [
        registro for registro in sistema.asistencias.values() if registro["docente"] == docente
    ]

    fila_metricas(
        [
            ("Cursos asignados", len(cursos)),
            ("Estudiantes", total_estudiantes),
            ("Calificaciones", len(calificaciones)),
            ("Asistencias", len(asistencias)),
        ]
    )
    fila_metricas(
        [
            ("Periodo activo", sistema.periodo_actual),
            ("Titulo", docente.titulo_profesional),
            ("Especialidad", docente.especialidad),
        ],
        columnas=3,
    )


def _consulta_docente(sistema, docente):
    cursos = _cursos_docente(sistema, docente)
    if not cursos:
        st.info("Este docente no tiene cursos asignados.")
        return

    st.markdown("#### Cursos asignados")
    tabla_o_vacio([curso_to_dict(curso) for curso in cursos], "Sin cursos.")

    calificaciones = [
        calificacion_registro_to_dict(registro)
        for registro in sistema.calificaciones.values()
        if registro["docente"] == docente
    ]
    st.markdown("#### Calificaciones registradas")
    tabla_o_vacio(calificaciones, "Sin calificaciones registradas.")


def mostrar_dashboard_docente(sistema):
    encabezado_pagina("Panel del docente", periodo=sistema.periodo_actual)

    docente = obtener_usuario_actual(sistema)
    if not docente:
        st.warning("No se encontro un docente seleccionado.")
        return

    st.markdown(f"### Bienvenido, {docente.nombres} {docente.apellidos}")

    tab_resumen, tab_consulta = st.tabs(["Resumen", "Consulta"])

    with tab_resumen:
        _resumen_docente(sistema, docente)
        cursos = _cursos_docente(sistema, docente)
        col1, col2, col3 = st.columns(3)
        with col1:
            metric_card("Cursos", len(cursos))
        with col2:
            metric_card("Estudiantes", sum(len(c.lista_estudiantes) for c in cursos))
        with col3:
            metric_card("Periodo", sistema.periodo_actual)

    with tab_consulta:
        _consulta_docente(sistema, docente)
