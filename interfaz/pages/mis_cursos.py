import streamlit as st

from interfaz.auth import obtener_rol_actual, obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.tables import curso_to_dict


def mostrar_mis_cursos(sistema):
    rol = obtener_rol_actual()
    usuario = obtener_usuario_actual(sistema)

    encabezado_pagina("Mis cursos")

    if not usuario:
        st.warning("No hay usuario seleccionado.")
        return

    if rol == "Docente":
        cursos = [curso for curso in sistema.cursos.values() if curso.docente == usuario]
        st.caption("Cursos asignados al docente en el periodo actual.")

    elif rol == "Estudiante":
        cursos = sistema.obtener_cursos_estudiante(usuario)
        st.caption("Cursos en los que el estudiante se encuentra inscrito.")

    else:
        cursos = []

    if not cursos:
        st.info("No hay cursos disponibles para este perfil.")
        return

    filas = [curso_to_dict(curso) for curso in cursos]
    st.dataframe(filas, use_container_width=True, hide_index=True)
