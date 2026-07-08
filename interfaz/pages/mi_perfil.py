import streamlit as st

from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.tables import usuario_to_dict


def mostrar_mi_perfil(sistema):
    encabezado_pagina("Mi perfil academico")

    estudiante = obtener_usuario_actual(sistema)

    if not estudiante:
        st.warning("No hay estudiante seleccionado.")
        return

    datos = usuario_to_dict(estudiante)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Datos personales")
        st.write(f"**Cedula:** {datos['Cedula']}")
        st.write(f"**Nombres:** {datos['Nombres']}")
        st.write(f"**Apellidos:** {datos['Apellidos']}")
        st.write(f"**Correo:** {datos['Correo']}")
        st.write(f"**Telefono:** {datos['Telefono']}")

    with col2:
        st.subheader("Datos academicos")
        st.write(f"**Tipo de usuario:** {datos['Tipo']}")
        st.write(f"**Estado:** {datos['Estado']}")
        st.write(
            f"**Estado de nivelacion:** "
            f"{getattr(estudiante, 'estado_nivelacion', 'No definido')}"
        )
