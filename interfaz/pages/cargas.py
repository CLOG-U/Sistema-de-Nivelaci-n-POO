import streamlit as st

from interfaz.branding import encabezado_pagina
from interfaz.components.layout import detalle_entidad, fila_metricas, intro_modulo, tabla_o_vacio
from interfaz.components.tables import carga_to_dict


def _formulario_carga(sistema):
    estudiantes = sistema.listar_estudiantes()
    if not estudiantes:
        st.warning("No hay estudiantes registrados.")
        return

    opciones_estudiantes = {f"{e.cedula} - {e.nombres} {e.apellidos}": e for e in estudiantes}

    with st.form("form_carga"):
        estudiante_etiqueta = st.selectbox("Estudiante", list(opciones_estudiantes.keys()))
        enviado = st.form_submit_button("Generar carga academica", use_container_width=True)

    if enviado:
        try:
            estudiante = opciones_estudiantes[estudiante_etiqueta]
            carga = sistema.registrar_carga_academica(estudiante)
            st.success(
                f"Carga generada para {estudiante.nombres} {estudiante.apellidos}. "
                f"Periodo: {carga.periodo}. "
                f"Asignaturas: {carga.total_asignaturas}. "
                f"Creditos: {carga.total_creditos}."
            )
        except Exception as error:
            st.error(str(error))


def _resumen_cargas(sistema):
    intro_modulo("Generacion y seguimiento de cargas academicas por periodo.", "📑")
    cargas = list(sistema.cargas_academicas.values())
    creditos = sum(c.total_creditos for c in cargas)
    asignaturas = sum(c.total_asignaturas for c in cargas)
    estudiantes_con_carga = len({c.estudiante.id_usuario for c in cargas})

    fila_metricas(
        [
            ("Cargas registradas", len(cargas)),
            ("Estudiantes con carga", estudiantes_con_carga),
            ("Total asignaturas", asignaturas),
            ("Total creditos", creditos),
        ]
    )


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
    encabezado_pagina("Cargas academicas")

    tab_resumen, tab_registrar, tab_consulta = st.tabs(["Resumen", "Registrar", "Consulta"])

    with tab_resumen:
        _resumen_cargas(sistema)

    with tab_registrar:
        intro_modulo("Genere la carga academica de un estudiante con cursos inscritos.", "📝")
        _formulario_carga(sistema)

    with tab_consulta:
        _consulta_cargas(sistema)
