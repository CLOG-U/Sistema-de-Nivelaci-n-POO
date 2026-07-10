import streamlit as st

from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.layout import intro_modulo
from interfaz.components.reportes_ui import panel_generar_reporte


def mostrar_reportes_estudiante(sistema):
    encabezado_pagina("Mis reportes academicos", periodo=sistema.periodo_actual)

    estudiante = obtener_usuario_actual(sistema)
    if not estudiante:
        st.warning("No hay estudiante seleccionado.")
        return

    intro_modulo(
        "Descargue su informacion academica personal: cursos, carga, calificaciones, asistencia "
        "o un resumen consolidado del periodo.",
        "📄",
    )
    panel_generar_reporte(sistema, "Estudiante", usuario=estudiante, prefijo="estudiante")
