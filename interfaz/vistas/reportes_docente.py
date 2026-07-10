import streamlit as st

from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.layout import intro_modulo
from interfaz.components.reportes_ui import panel_generar_reporte


def mostrar_reportes_docente(sistema):
    encabezado_pagina("Reportes del docente", periodo=sistema.periodo_actual)

    docente = obtener_usuario_actual(sistema)
    if not docente:
        st.warning("No hay docente seleccionado.")
        return

    intro_modulo(
        "Exporte reportes de sus cursos, calificaciones, asistencia y estudiantes inscritos. "
        "Solo se incluye informacion de los cursos que tiene asignados.",
        "📊",
    )
    panel_generar_reporte(sistema, "Docente", usuario=docente, prefijo="docente")
