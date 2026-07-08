import streamlit as st

from interfaz.auth import obtener_rol_actual, obtener_usuario_actual
from interfaz.branding import NOMBRE_SISTEMA, PERIODO_ACTUAL, encabezado_pagina
from interfaz.components.layout import fila_metricas, intro_modulo, tabla_o_vacio
from interfaz.components.tables import curso_to_dict


MODULOS_ADMIN = [
    ("Usuarios", "Gestion de estudiantes, docentes y administradores", "usuarios"),
    ("Aulas", "Registro y consulta de espacios fisicos", "aulas"),
    ("Horarios", "Planificacion de dias, horas y modalidad", "horarios"),
    ("Cursos", "Creacion de cursos de nivelacion", "cursos"),
    ("Inscripciones", "Matricula de estudiantes en cursos", "inscripciones"),
    ("Cargas Academicas", "Generacion de carga por periodo", "cargas"),
    ("Reportes", "Exportacion PDF y Excel", "reportes"),
]


def mostrar_dashboard(sistema):
    encabezado_pagina("Panel de administracion academica")

    rol = obtener_rol_actual()
    usuario = obtener_usuario_actual(sistema)

    if usuario:
        st.success(f"Sesion activa: {usuario.nombres} {usuario.apellidos} · Rol {rol}")
    else:
        st.info(f"Modo administracion · Periodo {PERIODO_ACTUAL}")

    intro_modulo(
        f"**{NOMBRE_SISTEMA}** · Resumen general del periodo activo. "
        "Utilice el menu lateral para gestionar cada modulo del sistema.",
        "📊",
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
            ("Cargas academicas", resumen.get("cargas", 0)),
            ("Reportes", resumen.get("reportes", 0)),
        ]
    )

    st.divider()
    st.subheader("Modulos del sistema")

    columnas = st.columns(2)
    for indice, (nombre, descripcion, _) in enumerate(MODULOS_ADMIN):
        with columnas[indice % 2]:
            with st.container(border=True):
                st.markdown(f"**{nombre}**")
                st.caption(descripcion)

    st.divider()
    st.subheader("Cursos activos del periodo")

    if not sistema.cursos:
        st.info("No hay cursos registrados en el periodo actual.")
        return

    filas = [curso_to_dict(curso) for curso in sistema.cursos.values()]
    tabla_o_vacio(filas, "Sin cursos para mostrar.")
