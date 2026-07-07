import streamlit as st

from interfaz.components.tables import usuario_to_dict


def mostrar_usuarios(sistema):
    st.title("Usuarios")
    st.subheader("Usuarios registrados")

    if not sistema.usuarios:
        st.warning("No hay usuarios registrados.")
        return

    filas = [usuario_to_dict(usuario) for usuario in sistema.usuarios]
    st.dataframe(filas, use_container_width=True, hide_index=True)
