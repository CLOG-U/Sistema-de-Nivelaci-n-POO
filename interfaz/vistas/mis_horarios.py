import streamlit as st

from interfaz.auth import obtener_rol_actual, obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.tables import horario_to_dict


def _cursos_por_usuario(sistema, rol, usuario):
    if rol == "Docente":
        return [curso for curso in sistema.cursos.values() if curso.docente == usuario]

    if rol == "Estudiante":
        return sistema.obtener_cursos_estudiante(usuario)

    return []


def mostrar_mis_horarios(sistema):
    rol = obtener_rol_actual()
    usuario = obtener_usuario_actual(sistema)

    encabezado_pagina("Mi horario" if rol == "Estudiante" else "Mis horarios")

    if not usuario:
        st.warning("No hay usuario seleccionado.")
        return

    cursos = _cursos_por_usuario(sistema, rol, usuario)
    horarios = []

    for curso in cursos:
        if curso.horario and curso.horario not in horarios:
            horarios.append(curso.horario)

    if not horarios:
        st.info("No hay horarios asignados para este perfil.")
        return

    filas = [horario_to_dict(horario) for horario in horarios]
    st.dataframe(filas, use_container_width=True, hide_index=True)
