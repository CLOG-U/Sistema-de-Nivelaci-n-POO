import streamlit as st

from interfaz.branding import encabezado_pagina
from interfaz.components.layout import detalle_entidad, fila_metricas, intro_modulo, tabla_o_vacio
from interfaz.components.tables import aula_con_uso_dict


def _cursos_por_aula(sistema, aula):
    return sum(1 for curso in sistema.cursos.values() if curso.aula == aula)


def _formulario_aula(sistema):
    with st.form("form_aula"):
        codigo = st.text_input("Codigo")
        nombre = st.text_input("Nombre")
        capacidad = st.number_input("Capacidad", min_value=1, step=1)
        piso = st.number_input("Piso", min_value=0, step=1)
        edificio = st.text_input("Edificio")
        enviado = st.form_submit_button("Registrar aula", use_container_width=True)

    if enviado:
        try:
            if not all([codigo, nombre, edificio]):
                raise ValueError("Complete todos los campos obligatorios")

            aula = sistema.registrar_aula(
                codigo.strip(),
                nombre.strip(),
                int(capacidad),
                int(piso),
                edificio.strip(),
            )
            st.success(f"Aula registrada: {aula.nombre}")
        except Exception as error:
            st.error(str(error))


def _resumen_aulas(sistema):
    intro_modulo("Administracion de aulas, capacidad y espacios asignados a cursos.", "🏫")
    aulas = list(sistema.aulas.values())
    capacidad_total = sum(aula.capacidad for aula in aulas)
    en_uso = sum(1 for aula in aulas if _cursos_por_aula(sistema, aula) > 0)

    fila_metricas(
        [
            ("Total aulas", len(aulas)),
            ("Capacidad total", capacidad_total),
            ("Aulas en uso", en_uso),
            ("Disponibles", len(aulas) - en_uso),
        ]
    )


def _consulta_aulas(sistema):
    aulas = list(sistema.aulas.values())
    if not aulas:
        st.warning("No hay aulas registradas.")
        return

    filtro_edificio = st.selectbox(
        "Filtrar por edificio",
        ["Todos"] + sorted({aula.edificio for aula in aulas}),
    )
    if filtro_edificio != "Todos":
        aulas = [a for a in aulas if a.edificio == filtro_edificio]

    filas = [
        aula_con_uso_dict(aula, _cursos_por_aula(sistema, aula)) for aula in aulas
    ]
    if not tabla_o_vacio(filas, "No hay aulas con ese filtro."):
        return

    for aula in aulas:
        detalle_entidad(
            f"{aula.codigo} · {aula.nombre}",
            [
                ("Capacidad", aula.capacidad),
                ("Piso", aula.piso),
                ("Edificio", aula.edificio),
                ("Estado", "Disponible" if aula.estado else "No disponible"),
                ("Cursos asignados", _cursos_por_aula(sistema, aula)),
            ],
        )


def mostrar_aulas(sistema):
    encabezado_pagina("Gestion de aulas")

    tab_resumen, tab_registrar, tab_consulta = st.tabs(["Resumen", "Registrar", "Consulta"])

    with tab_resumen:
        _resumen_aulas(sistema)

    with tab_registrar:
        intro_modulo("Registre nuevas aulas para asignarlas a horarios y cursos.", "📝")
        _formulario_aula(sistema)

    with tab_consulta:
        _consulta_aulas(sistema)
