import streamlit as st

from interfaz.branding import encabezado_pagina
from interfaz.components.tables import curso_to_dict


def _formulario_curso(sistema):
    st.subheader("Registrar curso")

    docentes = sistema.listar_docentes()
    if not docentes or not sistema.aulas or not sistema.horarios:
        st.warning("Debe existir al menos un docente, un aula y un horario para crear un curso.")
        return

    opciones_docentes = {f"{d.cedula} - {d.nombres} {d.apellidos}": d for d in docentes}
    opciones_aulas = {f"{a.codigo} - {a.nombre}": a for a in sistema.aulas}
    opciones_horarios = {
        f"{h.dia} {h.hora_inicio}-{h.hora_fin} ({h.aula.codigo})": h for h in sistema.horarios
    }

    with st.form("form_curso"):
        codigo = st.text_input("Codigo")
        nombre = st.text_input("Nombre")
        nivel = st.text_input("Nivel", value="Nivelacion")
        paralelo = st.text_input("Paralelo")
        cupo_maximo = st.number_input("Cupo maximo", min_value=1, step=1, value=30)
        docente_etiqueta = st.selectbox("Docente", list(opciones_docentes.keys()))
        horario_etiqueta = st.selectbox("Horario", list(opciones_horarios.keys()))
        aula_etiqueta = st.selectbox("Aula", list(opciones_aulas.keys()))

        enviado = st.form_submit_button("Registrar curso")

    if enviado:
        try:
            if not all([codigo, nombre, nivel, paralelo]):
                raise ValueError("Complete todos los campos obligatorios")

            curso = sistema.registrar_curso(
                codigo.strip(),
                nombre.strip(),
                nivel.strip(),
                paralelo.strip(),
                int(cupo_maximo),
                opciones_docentes[docente_etiqueta],
                opciones_horarios[horario_etiqueta],
                opciones_aulas[aula_etiqueta],
            )
            st.success(f"Curso registrado: {curso.nombre} (cupo {curso.cupo_actual}/{curso.cupo_maximo})")
        except Exception as error:
            st.error(str(error))


def mostrar_cursos(sistema):
    encabezado_pagina("Gestion de cursos de nivelacion")

    _formulario_curso(sistema)

    st.divider()
    st.subheader("Cursos de nivelacion")

    if not sistema.cursos:
        st.warning("No hay cursos registrados.")
        return

    filas = [curso_to_dict(curso) for curso in sistema.cursos]
    st.dataframe(filas, use_container_width=True, hide_index=True)
