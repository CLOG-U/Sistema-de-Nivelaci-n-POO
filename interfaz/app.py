import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import streamlit as st

from interfaz.auth import (
    cerrar_sesion,
    inicializar_sesion,
    obtener_rol_actual,
    obtener_usuario_actual,
    pantalla_seleccion_rol,
    usuarios_por_rol,
)
from interfaz.branding import TITULO_APP, encabezado_sidebar
from interfaz.navigation import obtener_opciones_por_rol
from interfaz.vistas.acerca import mostrar_acerca
from interfaz.vistas.aulas import mostrar_aulas
from interfaz.vistas.cargas import mostrar_cargas
from interfaz.vistas.cursos import mostrar_cursos
from interfaz.vistas.dashboard import mostrar_dashboard
from interfaz.vistas.dashboard_docente import mostrar_dashboard_docente
from interfaz.vistas.dashboard_estudiante import mostrar_dashboard_estudiante
from interfaz.vistas.estudiantes_docente import mostrar_estudiantes_docente
from interfaz.vistas.horarios import mostrar_horarios
from interfaz.vistas.inscripciones import mostrar_inscripciones
from interfaz.vistas.mi_carga import mostrar_mi_carga
from interfaz.vistas.mi_perfil import mostrar_mi_perfil
from interfaz.vistas.mis_cursos import mostrar_mis_cursos
from interfaz.vistas.mis_horarios import mostrar_mis_horarios
from interfaz.vistas.reportes import mostrar_reportes
from interfaz.vistas.reportes_docente import mostrar_reportes_docente
from interfaz.vistas.usuarios import mostrar_usuarios

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
    "Dashboard Docente": mostrar_dashboard_docente,
    "Mis Cursos": mostrar_mis_cursos,
    "Mis Horarios": mostrar_mis_horarios,
    "Estudiantes": mostrar_estudiantes_docente,
    "Reportes Docente": mostrar_reportes_docente,
    "Dashboard Estudiante": mostrar_dashboard_estudiante,
    "Mi Horario": mostrar_mis_horarios,
    "Mi Carga Academica": mostrar_mi_carga,
    "Mi Perfil": mostrar_mi_perfil,
}


def _selector_usuario_sidebar(sistema, rol):
    usuarios = usuarios_por_rol(sistema, rol)

    if not usuarios:
        st.sidebar.warning("No hay usuarios demo para este rol.")
        return

    opciones = {
        f"{u.nombres} {u.apellidos} · {u.cedula}": u.id_usuario for u in usuarios
    }

    usuario_actual_id = st.session_state.get("usuario_actual_id")
    valores = list(opciones.values())

    if usuario_actual_id not in valores:
        st.session_state.usuario_actual_id = valores[0]

    indice_actual = valores.index(st.session_state.usuario_actual_id)

    seleccionado = st.sidebar.selectbox(
        "Usuario demo",
        list(opciones.keys()),
        index=indice_actual,
    )

    st.session_state.usuario_actual_id = opciones[seleccionado]


def main():
    st.set_page_config(
        page_title=TITULO_APP,
        page_icon="🎓",
        layout="wide",
    )

    from interfaz.state import get_sistema
    from interfaz.styles import aplicar_estilos, pie_pagina

    aplicar_estilos()
    inicializar_sesion()

    sistema = get_sistema()
    rol = obtener_rol_actual()

    if not rol:
        st.sidebar.markdown(encabezado_sidebar(), unsafe_allow_html=True)
        pantalla_seleccion_rol(sistema)
        pie_pagina()
        return

    st.sidebar.markdown(encabezado_sidebar(), unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.caption("Sesion actual")
    st.sidebar.markdown(
        f'<span class="role-badge">Rol: {rol}</span>',
        unsafe_allow_html=True,
    )

    _selector_usuario_sidebar(sistema, rol)
    usuario = obtener_usuario_actual(sistema)

    if usuario:
        st.sidebar.info(f"{usuario.nombres} {usuario.apellidos}")

    if st.sidebar.button("Cambiar perfil", use_container_width=True):
        cerrar_sesion()

    st.sidebar.markdown("---")
    st.sidebar.caption("Menu de navegacion")

    opciones = obtener_opciones_por_rol(rol)
    if st.session_state.nav_seleccion not in opciones:
        st.session_state.nav_seleccion = opciones[0]

    indice_nav = opciones.index(st.session_state.nav_seleccion)
    opcion = st.sidebar.radio(
        "Navegacion",
        opciones,
        index=indice_nav,
        label_visibility="collapsed",
        key="nav_radio",
    )
    st.session_state.nav_seleccion = opcion

    RUTAS[opcion](sistema)
    pie_pagina()


main()
