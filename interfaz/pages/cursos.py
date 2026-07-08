import streamlit as st

from interfaz.branding import encabezado_pagina
from interfaz.components.layout import detalle_entidad, fila_metricas, intro_modulo, tabla_o_vacio
from interfaz.components.tables import curso_detalle_dict, usuario_to_dict


def _formulario_curso(sistema):
    docentes = sistema.listar_docentes()
    if not docentes or not sistema.aulas or not sistema.horarios:
        st.warning("Debe existir al menos un docente, un aula y un horario para crear un curso.")
        return

    opciones_docentes = {f"{d.cedula} - {d.nombres} {d.apellidos}": d for d in docentes}
    opciones_aulas = {f"{a.codigo} - {a.nombre}": a for a in sistema.aulas.values()}
    opciones_horarios = {
        f"{h.dia} {h.hora_inicio}-{h.hora_fin} ({h.aula.codigo})": h
        for h in sistema.horarios.values()
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
        enviado = st.form_submit_button("Registrar curso", use_container_width=True)

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


def _resumen_cursos(sistema):
    intro_modulo("Gestion de cursos de nivelacion con docente, horario y aula asignados.", "📚")
    cursos = list(sistema.cursos.values())
    inscritos = sistema.total_inscripciones()
    cupo_total = sum(c.cupo_maximo for c in cursos)
    cupo_usado = sum(c.cupo_actual for c in cursos)

    fila_metricas(
        [
            ("Cursos activos", len(cursos)),
            ("Estudiantes inscritos", inscritos),
            ("Cupo total", cupo_total),
            ("Cupo utilizado", cupo_usado),
        ]
    )


def _consulta_cursos(sistema):
    cursos = list(sistema.cursos.values())
    if not cursos:
        st.warning("No hay cursos registrados.")
        return

    filtro_docente = st.selectbox(
        "Filtrar por docente",
        ["Todos"] + [f"{d.nombres} {d.apellidos}" for d in sistema.listar_docentes()],
    )
    if filtro_docente != "Todos":
        cursos = [c for c in cursos if f"{c.docente.nombres} {c.docente.apellidos}" == filtro_docente]

    filas = [curso_detalle_dict(curso) for curso in cursos]
    if not tabla_o_vacio(filas, "No hay cursos con ese filtro."):
        return

    for curso in cursos:
        with st.expander(f"{curso.codigo} · {curso.nombre}", expanded=False):
            detalle_entidad(
                "Informacion del curso",
                [
                    ("Docente", f"{curso.docente.nombres} {curso.docente.apellidos}"),
                    ("Paralelo", curso.paralelo),
                    ("Cupo", f"{curso.cupo_actual}/{curso.cupo_maximo}"),
                    ("Horario", f"{curso.horario.dia} {curso.horario.hora_inicio}-{curso.horario.hora_fin}"),
                    ("Aula", f"{curso.aula.codigo} - {curso.aula.nombre}"),
                ],
            )
            if curso.lista_estudiantes:
                st.markdown("**Estudiantes inscritos**")
                inscritos = [usuario_to_dict(e) for e in curso.lista_estudiantes]
                st.dataframe(inscritos, use_container_width=True, hide_index=True)
            else:
                st.info("Sin estudiantes inscritos.")


def mostrar_cursos(sistema):
    encabezado_pagina("Gestion de cursos de nivelacion")

    tab_resumen, tab_registrar, tab_consulta = st.tabs(["Resumen", "Registrar", "Consulta"])

    with tab_resumen:
        _resumen_cursos(sistema)

    with tab_registrar:
        intro_modulo("Cree cursos vinculando docente, horario y aula.", "📝")
        _formulario_curso(sistema)

    with tab_consulta:
        _consulta_cursos(sistema)
