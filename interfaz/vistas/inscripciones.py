import streamlit as st

from interfaz.branding import encabezado_pagina
from interfaz.components.layout import fila_metricas, intro_modulo, tabla_o_vacio
from interfaz.components.tables import matricula_to_dict, periodo_to_dict, usuario_to_dict


def _formulario_inscripcion(sistema):
    estudiantes = sistema.listar_estudiantes()
    if not estudiantes:
        st.warning("No hay estudiantes registrados.")
        return
    if not sistema.cursos:
        st.warning("No hay cursos registrados.")
        return

    periodos_abiertos = sistema.listar_periodos_abiertos()
    if not periodos_abiertos:
        st.warning("No hay periodos academicos abiertos para matricular.")
        return

    opciones_estudiantes = {f"{e.cedula} - {e.nombres} {e.apellidos}": e for e in estudiantes}
    opciones_cursos = {f"{c.codigo} - {c.nombre}": c for c in sistema.cursos.values()}
    opciones_periodos = {
        f"{p.nombre} ({p.fecha_inicio} a {p.fecha_fin})": p for p in periodos_abiertos
    }

    with st.form("form_inscripcion"):
        estudiante_etiqueta = st.selectbox("Estudiante", list(opciones_estudiantes.keys()))
        curso_etiqueta = st.selectbox("Curso", list(opciones_cursos.keys()))
        periodo_etiqueta = st.selectbox("Periodo academico", list(opciones_periodos.keys()))
        tipo_matricula = st.selectbox("Tipo de matricula", ["Regular", "Extraordinaria", "Reintento"])
        enviado = st.form_submit_button("Matricular estudiante", use_container_width=True)

    if enviado:
        try:
            estudiante = opciones_estudiantes[estudiante_etiqueta]
            curso = opciones_cursos[curso_etiqueta]
            periodo = opciones_periodos[periodo_etiqueta]
            matricula = sistema.inscribir_estudiante(
                curso,
                estudiante,
                periodo=periodo,
                tipo_matricula=tipo_matricula,
            )
            st.success(
                f"Matricula completada para {estudiante.nombres} {estudiante.apellidos} "
                f"en {curso.nombre} (periodo {matricula.periodo}). "
                f"ID matricula: {matricula.id_matricula} | Tipo: {matricula.tipo_matricula} | "
                f"Cupo: {curso.cupo_actual}/{curso.cupo_maximo} | "
                f"Estado nivelacion: {estudiante.estado_nivelacion}"
            )
        except Exception as error:
            st.error(str(error))


def _resumen_inscripciones(sistema):
    intro_modulo(
        "Matricula de estudiantes mediante el patron Facade (MatriculaFacade + PeriodoAcademico).",
        "📋",
    )
    cursos = list(sistema.cursos.values())
    total_inscritos = sistema.total_inscripciones()
    total_matriculas = len(sistema.matriculas)
    cursos_con_cupo = sum(1 for c in cursos if c.cupo_actual < c.cupo_maximo)
    cursos_llenos = sum(1 for c in cursos if c.cupo_actual >= c.cupo_maximo)
    periodo_actual = sistema.obtener_periodo_actual()

    fila_metricas(
        [
            ("Cursos", len(cursos)),
            ("Inscripciones totales", total_inscritos),
            ("Matriculas registradas", total_matriculas),
            ("Cursos con cupo", cursos_con_cupo),
            ("Cupo completo", cursos_llenos),
        ]
    )

    if periodo_actual:
        st.markdown("#### Periodo academico actual")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Periodo", periodo_actual.nombre)
        with col2:
            st.metric("Estado", periodo_actual.estado)
        with col3:
            st.metric("Inicio", periodo_actual.fecha_inicio)
        with col4:
            st.metric("Fin", periodo_actual.fecha_fin)

    periodos = sistema.listar_periodos_academicos()
    if periodos:
        st.markdown("#### Periodos academicos")
        tabla_o_vacio([periodo_to_dict(p) for p in periodos], "Sin periodos registrados.")

    if cursos:
        resumen_cursos = {f"{c.codigo}": c.cupo_actual for c in cursos}
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
        fila.update(matricula_to_dict(estudiante.matricula))
        filas.append(fila)

    tabla_o_vacio(filas, "Sin inscritos.")


def _formulario_periodo(sistema):
    with st.form("form_periodo_inscripciones"):
        nombre = st.text_input("Nombre del periodo", placeholder="2027-1")
        fecha_inicio = st.text_input("Fecha inicio (AAAA-MM-DD)", value="2027-01-01")
        fecha_fin = st.text_input("Fecha fin (AAAA-MM-DD)", value="2027-06-30")
        estado = st.selectbox("Estado inicial", ["Abierto", "Cerrado"])
        enviado = st.form_submit_button("Registrar periodo", use_container_width=True)

    if enviado:
        try:
            periodo = sistema.registrar_periodo(
                nombre.strip(),
                fecha_inicio.strip(),
                fecha_fin.strip(),
                estado,
            )
            st.success(f"Periodo {periodo.nombre} registrado.")
        except Exception as error:
            st.error(str(error))


def _gestionar_periodo_actual(sistema):
    periodos = sistema.listar_periodos_academicos()
    if not periodos:
        return

    opciones = {f"{p.nombre} ({p.estado})": p.nombre for p in periodos}
    col1, col2, col3 = st.columns(3)

    with col1:
        seleccion = st.selectbox("Periodo activo del sistema", list(opciones.keys()))
        if st.button("Establecer como activo", use_container_width=True):
            try:
                periodo = sistema.establecer_periodo_actual(opciones[seleccion])
                st.success(f"Periodo activo: {periodo.nombre}")
            except Exception as error:
                st.error(str(error))

    with col2:
        if st.button("Abrir periodo seleccionado", use_container_width=True):
            try:
                periodo = sistema.abrir_periodo(opciones[seleccion])
                st.success(f"Periodo {periodo.nombre} abierto.")
            except Exception as error:
                st.error(str(error))

    with col3:
        if st.button("Cerrar periodo seleccionado", use_container_width=True):
            try:
                periodo = sistema.cerrar_periodo(opciones[seleccion])
                st.success(f"Periodo {periodo.nombre} cerrado.")
            except Exception as error:
                st.error(str(error))


def mostrar_inscripciones(sistema):
    encabezado_pagina("Inscripciones academicas", periodo=sistema.periodo_actual)

    tab_resumen, tab_registrar, tab_consulta = st.tabs(["Resumen", "Registrar", "Consulta"])

    with tab_resumen:
        _resumen_inscripciones(sistema)
        st.markdown("#### Gestion de periodos")
        _gestionar_periodo_actual(sistema)

    with tab_registrar:
        intro_modulo(
            "Matricule estudiantes en cursos abiertos usando MatriculaFacade y un periodo academico activo.",
            "📝",
        )
        _formulario_inscripcion(sistema)
        with st.expander("Registrar nuevo periodo academico"):
            _formulario_periodo(sistema)

    with tab_consulta:
        _consulta_inscritos(sistema)
