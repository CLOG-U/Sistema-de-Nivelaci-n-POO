import streamlit as st

from interfaz.auth import obtener_rol_actual, obtener_usuario_actual
from interfaz.branding import NOMBRE_SISTEMA, encabezado_pagina
from interfaz.components.layout import fila_metricas, intro_modulo, tabla_o_vacio
from interfaz.components.tables import curso_to_dict

MODULOS_ADMIN = [
    ("Usuarios", "Gestion de estudiantes, docentes y administradores"),
    ("Aulas", "Registro y consulta de espacios fisicos"),
    ("Horarios", "Planificacion de dias, horas y modalidad"),
    ("Cursos", "Creacion de cursos de nivelacion"),
    ("Inscripciones", "Matricula de estudiantes en cursos"),
    ("Cargas Academicas", "Generacion de carga por periodo"),
    ("Reportes", "Exportacion PDF y Excel"),
]


def mostrar_dashboard(sistema):
    encabezado_pagina("Panel de administracion academica", periodo=sistema.periodo_actual)

    rol = obtener_rol_actual()
    usuario = obtener_usuario_actual(sistema)
    periodo_actual = sistema.obtener_periodo_actual()

    if usuario:
        st.success(f"Sesion activa: {usuario.nombres} {usuario.apellidos} · Rol {rol}")
    else:
        st.info(f"Modo administracion · Periodo {sistema.periodo_actual}")

    intro_modulo(
        f"**{NOMBRE_SISTEMA}** · Resumen general del periodo activo. "
        "Seleccione un modulo para ir directamente a su gestion.",
        "📊",
    )

    if periodo_actual:
        fila_metricas(
            [
                ("Periodo activo", periodo_actual.nombre),
                ("Estado periodo", periodo_actual.estado),
                ("Periodos registrados", len(sistema.periodos)),
            ],
            columnas=3,
        )

    resumen = sistema.resumen()
    fila_metricas(
        [
            ("Usuarios", resumen.get("usuarios", 0)),
            ("Docentes", resumen.get("docentes", 0)),
            ("Estudiantes", resumen.get("estudiantes", 0)),
            ("Cursos", resumen.get("cursos", 0)),
        ]
    )
    fila_metricas(
        [
            ("Aulas", resumen.get("aulas", 0)),
            ("Inscripciones", sistema.total_inscripciones()),
            ("Calificaciones", resumen.get("calificaciones", 0)),
            ("Asistencias", resumen.get("asistencias", 0)),
        ]
    )
    fila_metricas(
        [
            ("Cargas academicas", resumen.get("cargas", 0)),
            ("Reportes", resumen.get("reportes", 0)),
            ("Matriculas", resumen.get("matriculas", 0)),
        ],
        columnas=3,
    )

    st.divider()
    st.subheader("Modulos del sistema")

    columnas = st.columns(2)
    for indice, (nombre, descripcion) in enumerate(MODULOS_ADMIN):
        with columnas[indice % 2]:
            with st.container(border=True):
                st.markdown(f"**{nombre}**")
                st.caption(descripcion)
                if st.button(f"Ir a {nombre}", key=f"modulo_{nombre}", use_container_width=True):
                    st.session_state.nav_seleccion = nombre
                    st.rerun()

    st.divider()
    st.subheader("Cursos activos del periodo")

    if not sistema.cursos:
        st.info("No hay cursos registrados en el periodo actual.")
        return

    filas = [curso_to_dict(curso) for curso in sistema.cursos.values()]
    tabla_o_vacio(filas, "Sin cursos para mostrar.")
