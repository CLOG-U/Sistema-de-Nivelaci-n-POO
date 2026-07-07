import streamlit as st

from interfaz.pages.acerca import mostrar_acerca
from interfaz.pages.aulas import mostrar_aulas
from interfaz.pages.cargas import mostrar_cargas
from interfaz.pages.cursos import mostrar_cursos
from interfaz.pages.dashboard import mostrar_dashboard
from interfaz.pages.horarios import mostrar_horarios
from interfaz.pages.inscripciones import mostrar_inscripciones
from interfaz.pages.reportes import mostrar_reportes
from interfaz.pages.usuarios import mostrar_usuarios

OPCIONES = [
    "Dashboard",
    "Usuarios",
    "Aulas",
    "Horarios",
    "Cursos",
    "Inscripciones",
    "Cargas Academicas",
    "Reportes",
    "Acerca del Sistema",
]

RUTAS = {
    "Dashboard": mostrar_dashboard,
    "Usuarios": mostrar_usuarios,
    "Aulas": mostrar_aulas,
    "Horarios": mostrar_horarios,
    "Cursos": mostrar_cursos,
    "Inscripciones": mostrar_inscripciones,
    "Cargas Academicas": mostrar_cargas,
    "Reportes": mostrar_reportes,
    "Acerca del Sistema": mostrar_acerca,
}


def main():
    st.set_page_config(page_title="Sistema de Nivelacion POO", layout="wide")

    from interfaz.state import get_sistema
    from interfaz.styles import aplicar_estilos

    aplicar_estilos()
    sistema = get_sistema()

    st.sidebar.title("Menu")
    st.sidebar.caption("Sistema de Nivelacion POO")
    opcion = st.sidebar.radio("Navegacion", OPCIONES)

    RUTAS[opcion](sistema)


main()
