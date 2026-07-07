import streamlit as st

from interfaz.branding import encabezado_pagina
from interfaz.components.tables import usuario_to_dict


def _formulario_inscripcion(sistema):
    st.subheader("Inscribir estudiante en curso")

    estudiantes = sistema.listar_estudiantes()
    if not estudiantes:
        st.warning("No hay estudiantes registrados.")
        return
    if not sistema.cursos:
        st.warning("No hay cursos registrados.")
        return

    opciones_estudiantes = {f"{e.cedula} - {e.nombres} {e.apellidos}": e for e in estudiantes}
    opciones_cursos = {f"{c.codigo} - {c.nombre}": c for c in sistema.cursos}

    with st.form("form_inscripcion"):
        estudiante_etiqueta = st.selectbox("Estudiante", list(opciones_estudiantes.keys()))
        curso_etiqueta = st.selectbox("Curso", list(opciones_cursos.keys()))
        enviado = st.form_submit_button("Inscribir estudiante")

    if enviado:
        try:
            estudiante = opciones_estudiantes[estudiante_etiqueta]
            curso = opciones_cursos[curso_etiqueta]
            sistema.inscribir_estudiante(curso, estudiante)
            st.success(
                f"Estudiante inscrito en {curso.nombre}. "
                f"Cupo: {curso.cupo_actual}/{curso.cupo_maximo}. "
                f"Estado: {estudiante.estado_nivelacion}"
            )
        except Exception as error:
            st.error(str(error))


def _tabla_inscritos_por_curso(sistema):
    st.subheader("Estudiantes inscritos por curso")

    if not sistema.cursos:
        st.warning("No hay cursos registrados.")
        return

    opciones_cursos = {f"{c.codigo} - {c.nombre}": c for c in sistema.cursos}
    curso_etiqueta = st.selectbox("Seleccione un curso", list(opciones_cursos.keys()), key="curso_inscritos")
    curso = opciones_cursos[curso_etiqueta]

    if not curso.lista_estudiantes:
        st.info("Este curso no tiene estudiantes inscritos.")
        return

    filas = []
    for estudiante in curso.lista_estudiantes:
        fila = usuario_to_dict(estudiante)
        fila["Estado nivelacion"] = estudiante.estado_nivelacion
        filas.append(fila)

    st.dataframe(filas, use_container_width=True, hide_index=True)


def mostrar_inscripciones(sistema):
    encabezado_pagina("Inscripciones academicas")

    _formulario_inscripcion(sistema)
    st.divider()
    _tabla_inscritos_por_curso(sistema)
