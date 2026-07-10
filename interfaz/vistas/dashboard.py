import streamlit as st

from interfaz.auth import obtener_rol_actual, obtener_usuario_actual
from interfaz.branding import NOMBRE_SISTEMA, encabezado_pagina
from interfaz.components.layout import fila_metricas, intro_modulo, tabla_o_vacio, tarjetas_navegacion
from interfaz.components.tables import curso_to_dict
from interfaz.navigation import modulos_admin_traducidos


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
    tarjetas_navegacion(modulos_admin_traducidos(), prefijo_clave="admin")

    st.divider()
    st.subheader("Cursos activos del periodo")

    if not sistema.cursos:
        st.info("No hay cursos registrados en el periodo actual.")
        return

    filas = [curso_to_dict(curso) for curso in sistema.cursos.values()]
    tabla_o_vacio(filas, "Sin cursos para mostrar.")
