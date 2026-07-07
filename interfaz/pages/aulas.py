import streamlit as st

from interfaz.branding import encabezado_pagina
from interfaz.components.tables import aula_to_dict


def _formulario_aula(sistema):
    st.subheader("Registrar aula")

    with st.form("form_aula"):
        codigo = st.text_input("Codigo")
        nombre = st.text_input("Nombre")
        capacidad = st.number_input("Capacidad", min_value=1, step=1)
        piso = st.number_input("Piso", min_value=0, step=1)
        edificio = st.text_input("Edificio")

        enviado = st.form_submit_button("Registrar aula")

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


def mostrar_aulas(sistema):
    encabezado_pagina("Gestion de aulas")

    _formulario_aula(sistema)

    st.divider()
    st.subheader("Aulas registradas")

    if not sistema.aulas:
        st.warning("No hay aulas registradas.")
        return

    filas = [aula_to_dict(aula) for aula in sistema.aulas]
    st.dataframe(filas, use_container_width=True, hide_index=True)
