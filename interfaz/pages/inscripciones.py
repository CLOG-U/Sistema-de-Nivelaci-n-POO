import streamlit as st

from interfaz.branding import encabezado_pagina
from interfaz.components.layout import fila_metricas, intro_modulo, tabla_o_vacio
from interfaz.components.tables import usuario_to_dict


def _formulario_inscripcion(sistema):
    estudiantes = sistema.listar_estudiantes()
    if not estudiantes:
        st.warning("No hay estudiantes registrados.")
        return
    if not sistema.cursos:
        st.warning("No hay cursos registrados.")
        return

    opciones_estudiantes = {f"{e.cedula} - {e.nombres} {e.apellidos}": e for e in estudiantes}
    opciones_cursos = {f"{c.codigo} - {c.nombre}": c for c in sistema.cursos.values()}

    with st.form("form_inscripcion"):
        estudiante_etiqueta = st.selectbox("Estudiante", list(opciones_estudiantes.keys()))
        curso_etiqueta = st.selectbox("Curso", list(opciones_cursos.keys()))
        enviado = st.form_submit_button("Inscribir estudiante", use_container_width=True)

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


def _resumen_inscripciones(sistema):
    intro_modulo("Matricula de estudiantes en cursos de nivelacion del periodo.", "📋")
    cursos = list(sistema.cursos.values())
    total_inscritos = sistema.total_inscripciones()
    cursos_con_cupo = sum(1 for c in cursos if c.cupo_actual < c.cupo_maximo)
    cursos_llenos = sum(1 for c in cursos if c.cupo_actual >= c.cupo_maximo)

    fila_metricas(
        [
            ("Cursos", len(cursos)),
            ("Inscripciones totales", total_inscritos),
            ("Con cupo disponible", cursos_con_cupo),
            ("Cupo completo", cursos_llenos),
        ]
    )

    if cursos:
        resumen_cursos = {
            f"{c.codigo}": c.cupo_actual for c in cursos
        }
        st.markdown("#### Inscritos por curso")
        st.bar_chart(resumen_cursos)


def _consulta_inscritos(sistema):
    cursos = list(sistema.cursos.values())
    if not cursos:
        st.warning("No hay cursos registrados.")
        return

    opciones_cursos = {f"{c.codigo} - {c.nombre}": c for c in cursos}
    curso_etiqueta = st.selectbox("Seleccione un curso", list(opciones_cursos.keys()), key="curso_inscritos")
    curso = opciones_cursos[curso_etiqueta]

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Cupo maximo", curso.cupo_maximo)
    with col2:
        st.metric("Inscritos", curso.cupo_actual)
    with col3:
        st.metric("Disponibles", curso.cupo_maximo - curso.cupo_actual)

    if not curso.lista_estudiantes:
        st.info("Este curso no tiene estudiantes inscritos.")
        return

    filas = []
    for estudiante in curso.lista_estudiantes:
        fila = usuario_to_dict(estudiante)
        fila["Estado nivelacion"] = estudiante.estado_nivelacion
        filas.append(fila)

    tabla_o_vacio(filas, "Sin inscritos.")


def mostrar_inscripciones(sistema):
    encabezado_pagina("Inscripciones academicas")

    tab_resumen, tab_registrar, tab_consulta = st.tabs(["Resumen", "Registrar", "Consulta"])

    with tab_resumen:
        _resumen_inscripciones(sistema)

    with tab_registrar:
        intro_modulo("Inscriba estudiantes en los cursos disponibles.", "📝")
        _formulario_inscripcion(sistema)

    with tab_consulta:
        _consulta_inscritos(sistema)
