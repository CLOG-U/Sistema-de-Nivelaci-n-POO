import streamlit as st

from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.layout import tabla_o_vacio
from interfaz.components.tables import (
    asistencia_registro_to_dict,
    calificacion_registro_to_dict,
    usuario_to_dict,
)


def mostrar_mi_perfil(sistema):
    encabezado_pagina("Mi perfil academico", periodo=sistema.periodo_actual)

    estudiante = obtener_usuario_actual(sistema)
    if not estudiante:
        st.warning("No hay estudiante seleccionado.")
        return

    datos = usuario_to_dict(estudiante)
    calificaciones = sistema.obtener_calificaciones_estudiante(estudiante)
    asistencias = sistema.obtener_asistencias_estudiante(estudiante)

    tab_perfil, tab_calificaciones, tab_asistencia = st.tabs(
        ["Perfil", "Calificaciones", "Asistencia"]
    )

    with tab_perfil:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Datos personales")
            st.write(f"**Cedula:** {datos['Cedula']}")
            st.write(f"**Nombres:** {datos['Nombres']}")
            st.write(f"**Apellidos:** {datos['Apellidos']}")
            st.write(f"**Correo:** {datos['Correo']}")
            st.write(f"**Telefono:** {datos['Telefono']}")

        with col2:
            st.subheader("Datos academicos")
            st.write(f"**Tipo de usuario:** {datos['Tipo']}")
            st.write(f"**Estado:** {datos['Estado']}")
            st.write(f"**Estado de nivelacion:** {estudiante.estado_nivelacion}")
            st.write(f"**Periodo activo:** {sistema.periodo_actual}")
            if estudiante.matricula:
                st.write(f"**Ultima matricula:** {estudiante.matricula.periodo}")

    with tab_calificaciones:
        st.subheader("Mis calificaciones")
        tabla_o_vacio(
            [calificacion_registro_to_dict(registro) for registro in calificaciones],
            "Aun no tienes calificaciones registradas.",
        )

    with tab_asistencia:
        st.subheader("Mi asistencia")
        tabla_o_vacio(
            [asistencia_registro_to_dict(registro) for registro in asistencias],
            "Aun no tienes registros de asistencia.",
        )
