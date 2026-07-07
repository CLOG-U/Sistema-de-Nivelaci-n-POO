import streamlit as st

from interfaz.components.tables import curso_to_dict


def mostrar_cursos(sistema):
    st.title("Cursos")
    st.subheader("Cursos de nivelacion")

    if not sistema.cursos:
        st.warning("No hay cursos registrados.")
        return

    filas = [curso_to_dict(curso) for curso in sistema.cursos]
    st.dataframe(filas, use_container_width=True, hide_index=True)
