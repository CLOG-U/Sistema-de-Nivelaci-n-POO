import streamlit as st

from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.tables import usuario_to_dict


def mostrar_estudiantes_docente(sistema):
    encabezado_pagina("Mis estudiantes")

    docente = obtener_usuario_actual(sistema)

    if not docente:
        st.warning("No hay docente seleccionado.")
        return

    cursos_docente = [
        curso for curso in sistema.cursos.values() if curso.docente == docente
    ]

    if not cursos_docente:
        st.info("Este docente no tiene cursos asignados.")
        return

    opciones = {
        f"{curso.codigo} - {curso.nombre}": curso for curso in cursos_docente
    }

    curso_etiqueta = st.selectbox("Seleccione un curso", list(opciones.keys()))
    curso = opciones[curso_etiqueta]

    if not curso.lista_estudiantes:
        st.info("Este curso no tiene estudiantes inscritos.")
        return

    filas = []
    for estudiante in curso.lista_estudiantes:
        fila = usuario_to_dict(estudiante)
        fila["Estado nivelacion"] = estudiante.estado_nivelacion
        filas.append(fila)

    st.dataframe(filas, use_container_width=True, hide_index=True)
