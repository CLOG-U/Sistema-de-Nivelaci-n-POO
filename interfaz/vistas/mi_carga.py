import streamlit as st

from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.tables import carga_to_dict


def mostrar_mi_carga(sistema):
    encabezado_pagina("Mi carga academica")

    estudiante = obtener_usuario_actual(sistema)

    if not estudiante:
        st.warning("No hay estudiante seleccionado.")
        return

    cargas = [
        carga
        for carga in sistema.cargas_academicas.values()
        if carga.estudiante == estudiante
    ]

    if not cargas:
        st.info("Todavia no tienes una carga academica registrada.")
        return

    filas = [carga_to_dict(carga) for carga in cargas]
    st.dataframe(filas, use_container_width=True, hide_index=True)
