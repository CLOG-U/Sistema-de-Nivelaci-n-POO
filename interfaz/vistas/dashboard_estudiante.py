import streamlit as st

from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.cards import metric_card
from interfaz.components.layout import fila_metricas, intro_modulo, tabla_o_vacio, tarjetas_navegacion
from interfaz.components.tables import (
    asistencia_registro_to_dict,
    calificacion_registro_to_dict,
    carga_to_dict,
    curso_to_dict,
)
from interfaz.navigation import modulos_estudiante_traducidos


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


def _resumen_estudiante(sistema, estudiante):
    intro_modulo("Resumen personal del estudiante en el periodo activo.", "🎓")
    cursos = _cursos_estudiante(sistema, estudiante)
    cargas = _cargas_estudiante(sistema, estudiante)
    calificaciones = sistema.obtener_calificaciones_estudiante(estudiante)
    asistencias = sistema.obtener_asistencias_estudiante(estudiante)

    fila_metricas(
        [
            ("Cursos inscritos", len(cursos)),
            ("Estado nivelacion", estudiante.estado_nivelacion),
            ("Calificaciones", len(calificaciones)),
            ("Asistencias", len(asistencias)),
        ]
    )
    fila_metricas(
        [
            ("Cargas academicas", len(cargas)),
            ("Periodo activo", sistema.periodo_actual),
        ],
        columnas=2,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        metric_card("Cursos", len(cursos))
    with col2:
        metric_card("Estado", estudiante.estado_nivelacion)
    with col3:
        metric_card("Periodo", sistema.periodo_actual)

    st.divider()
    st.subheader("Accesos rapidos")
    tarjetas_navegacion(modulos_estudiante_traducidos(), prefijo_clave="estudiante")


def _consulta_estudiante(sistema, estudiante):
    cursos = _cursos_estudiante(sistema, estudiante)
    cargas = _cargas_estudiante(sistema, estudiante)
    calificaciones = sistema.obtener_calificaciones_estudiante(estudiante)
    asistencias = sistema.obtener_asistencias_estudiante(estudiante)

    st.markdown("#### Mis cursos")
    tabla_o_vacio([curso_to_dict(curso) for curso in cursos], "Todavia no tienes cursos inscritos.")

    st.markdown("#### Mi carga academica")
    tabla_o_vacio([carga_to_dict(carga) for carga in cargas], "Sin carga academica generada.")

    st.markdown("#### Mis calificaciones")
    tabla_o_vacio(
        [calificacion_registro_to_dict(registro) for registro in calificaciones],
        "Sin calificaciones registradas.",
    )

    st.markdown("#### Mi asistencia")
    tabla_o_vacio(
        [asistencia_registro_to_dict(registro) for registro in asistencias],
        "Sin registros de asistencia.",
    )


def mostrar_dashboard_estudiante(sistema):
    encabezado_pagina("Panel del estudiante", periodo=sistema.periodo_actual)

    estudiante = obtener_usuario_actual(sistema)
    if not estudiante:
        st.warning("No se encontro un estudiante seleccionado.")
        return

    st.markdown(f"### Bienvenido, {estudiante.nombres} {estudiante.apellidos}")

    tab_resumen, tab_consulta = st.tabs(["Resumen", "Consulta"])

    with tab_resumen:
        _resumen_estudiante(sistema, estudiante)

    with tab_consulta:
        _consulta_estudiante(sistema, estudiante)
