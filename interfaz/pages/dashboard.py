import streamlit as st

from interfaz.components.cards import metric_card


def mostrar_dashboard(sistema):
    st.title("Sistema de Nivelacion POO")
    st.subheader("Panel de administracion academica")

    resumen = sistema.resumen()
    etiquetas = {
        "usuarios": "Usuarios",
        "docentes": "Docentes",
        "estudiantes": "Estudiantes",
        "cursos": "Cursos",
        "aulas": "Aulas",
        "cargas": "Cargas academicas",
        "reportes": "Reportes",
    }

    columnas = st.columns(4)
    for indice, (clave, etiqueta) in enumerate(etiquetas.items()):
        with columnas[indice % 4]:
            metric_card(etiqueta, resumen.get(clave, 0))
