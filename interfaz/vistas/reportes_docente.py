import streamlit as st

from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina


def mostrar_reportes_docente(sistema):
    encabezado_pagina("Reportes del docente")

    docente = obtener_usuario_actual(sistema)

    if not docente:
        st.warning("No hay docente seleccionado.")
        return

    cursos = [curso for curso in sistema.cursos.values() if curso.docente == docente]

    st.caption(
        "Vista de reportes academicos del docente. No permite gestion administrativa."
    )

    if not cursos:
        st.info("No hay informacion academica para generar reportes.")
        return

    resumen = []

    for curso in cursos:
        horario_texto = "Sin horario"
        if curso.horario:
            horario_texto = (
                f"{curso.horario.dia} "
                f"{curso.horario.hora_inicio}-{curso.horario.hora_fin}"
            )

        resumen.append(
            {
                "Curso": curso.nombre,
                "Codigo": curso.codigo,
                "Paralelo": curso.paralelo,
                "Cupo": f"{curso.cupo_actual}/{curso.cupo_maximo}",
                "Estudiantes inscritos": len(curso.lista_estudiantes),
                "Horario": horario_texto,
            }
        )

    st.dataframe(resumen, use_container_width=True, hide_index=True)
