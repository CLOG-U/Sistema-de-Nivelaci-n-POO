import streamlit as st

from interfaz.branding import encabezado_pagina
from interfaz.components.layout import detalle_entidad, fila_metricas, intro_modulo, tabla_o_vacio
from interfaz.components.tables import carga_to_dict, periodo_to_dict


def _formulario_carga(sistema): 
    estudiantes = sistema.listar_estudiantes()   # Formulario para generar una carga académica.
    if not estudiantes:
        st.warning("No hay estudiantes registrados.")
        return

    periodos_abiertos = sistema.listar_periodos_abiertos()
    if not periodos_abiertos:
        st.warning("No hay periodos academicos abiertos.")
        return

    opciones_estudiantes = {f"{e.cedula} - {e.nombres} {e.apellidos}": e for e in estudiantes} # Opciones para los selectores.
    opciones_periodos = {f"{p.nombre} ({p.estado})": p.nombre for p in periodos_abiertos}

    with st.form("form_carga"):
        estudiante_etiqueta = st.selectbox("Estudiante", list(opciones_estudiantes.keys()))
        periodo_etiqueta = st.selectbox("Periodo academico", list(opciones_periodos.keys()))
        enviado = st.form_submit_button("Generar carga academica", use_container_width=True)

    if enviado:
        try:
            estudiante = opciones_estudiantes[estudiante_etiqueta] # Genera la carga académica.
            periodo = opciones_periodos[periodo_etiqueta]
            carga = sistema.registrar_carga_academica(estudiante, periodo=periodo)
            st.success(
                f"Carga generada para {estudiante.nombres} {estudiante.apellidos}. "
                f"Periodo: {carga.periodo}. "
                f"Asignaturas: {carga.total_asignaturas}. "
                f"Creditos: {carga.total_creditos}."
            )
        except Exception as error:
            st.error(str(error)) # Muestra el error.


def _formulario_periodo(sistema): # Formulario para registrar un periodo académico.
    with st.form("form_periodo_cargas"):
        nombre = st.text_input("Nombre del periodo", placeholder="2026-2")
        fecha_inicio = st.text_input("Fecha inicio (AAAA-MM-DD)", value="2026-07-01")
        fecha_fin = st.text_input("Fecha fin (AAAA-MM-DD)", value="2026-12-15")
        estado = st.selectbox("Estado inicial", ["Abierto", "Cerrado"])
        enviado = st.form_submit_button("Registrar periodo", use_container_width=True)

    if enviado:
        try:
            periodo = sistema.registrar_periodo( # Registra el periodo.
                nombre.strip(),
                fecha_inicio.strip(),
                fecha_fin.strip(),
                estado,
            )
            st.success(f"Periodo {periodo.nombre} registrado con estado {periodo.estado}")
        except Exception as error:
            st.error(str(error))  # Muestra el error.


def _resumen_cargas(sistema): # Muestra el resumen de cargas académicas.
    intro_modulo("Generacion y seguimiento de cargas academicas por periodo academico.", "📑")
    cargas = list(sistema.cargas_academicas.values())
    creditos = sum(c.total_creditos for c in cargas)
    asignaturas = sum(c.total_asignaturas for c in cargas)
    estudiantes_con_carga = len({c.estudiante.id_usuario for c in cargas})

    fila_metricas( # Muestra métricas.
        [
            ("Cargas registradas", len(cargas)),
            ("Estudiantes con carga", estudiantes_con_carga),
            ("Total asignaturas", asignaturas),
            ("Total creditos", creditos),
        ]
    )

    periodos = sistema.listar_periodos_academicos()
    if periodos:
        st.markdown("#### Periodos disponibles")
        tabla_o_vacio([periodo_to_dict(p) for p in periodos], "Sin periodos.")

# Consulta las cargas académicas.
def _consulta_cargas(sistema):
    cargas = list(sistema.cargas_academicas.values())
    if not cargas:
        st.warning("No hay cargas academicas registradas.")
        return

    filtro_periodo = st.selectbox(
        "Filtrar por periodo",
        ["Todos"] + sorted({c.periodo for c in cargas}),
    )
    if filtro_periodo != "Todos":
        cargas = [c for c in cargas if c.periodo == filtro_periodo]

    filas = [carga_to_dict(carga) for carga in cargas]
    if not tabla_o_vacio(filas, "No hay cargas con ese filtro."):
        return

    for carga in cargas:
        estudiante = carga.estudiante
        cursos = sistema.obtener_cursos_estudiante(estudiante)
        detalle_entidad(
            f"{estudiante.nombres} {estudiante.apellidos} · {carga.periodo}",
            [
                ("Asignaturas", carga.total_asignaturas),
                ("Creditos", carga.total_creditos),
                ("Estado", "Activa" if carga.estado else "Inactiva"),
                ("Cursos inscritos", ", ".join(c.codigo for c in cursos) or "Ninguno"),
            ],
        )


def mostrar_cargas(sistema):
    encabezado_pagina("Cargas academicas", periodo=sistema.periodo_actual)

    tab_resumen, tab_registrar, tab_consulta = st.tabs(["Resumen", "Registrar", "Consulta"])

    with tab_resumen:
        _resumen_cargas(sistema)

    with tab_registrar:
        intro_modulo("Genere cargas por periodo academico seleccionado.", "📝")
        _formulario_carga(sistema)
        with st.expander("Registrar nuevo periodo academico"):
            _formulario_periodo(sistema)

    with tab_consulta:
        _consulta_cargas(sistema)
