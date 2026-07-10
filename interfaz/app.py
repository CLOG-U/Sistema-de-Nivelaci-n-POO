import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import streamlit as st

from interfaz.auth import (
    cerrar_sesion,
    esta_autenticado,
    inicializar_sesion,
    obtener_rol_actual,
    obtener_usuario_actual,
    pantalla_login,
)
from interfaz.branding import TITULO_APP, encabezado_sidebar, mostrar_logo_sidebar, RUTA_LOGO
from interfaz.idioma import obtener_gestor_idioma, selector_idioma, t
from interfaz.navigation import (
    dashboard_inicial_por_rol,
    es_opcion_permitida,
    obtener_etiquetas_menu,
    obtener_opciones_por_rol,
)
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
    "Cargas": mostrar_cargas,
    "Reportes": mostrar_reportes,
    "Acerca del Sistema": mostrar_acerca,
    "Dashboard Docente": mostrar_dashboard_docente,
    "Mis Cursos": mostrar_mis_cursos,
    "Mis Horarios": mostrar_mis_horarios,
    "Mis Estudiantes": mostrar_estudiantes_docente,
    "Reportes Docente": mostrar_reportes_docente,
    "Dashboard Estudiante": mostrar_dashboard_estudiante,
    "Mi Horario": mostrar_mis_horarios,
    "Mi Carga": mostrar_mi_carga,
    "Mi Perfil": mostrar_mi_perfil,
}


def _render_sidebar_sesion(sistema, rol, usuario):
    gestor = obtener_gestor_idioma()

    mostrar_logo_sidebar()
    st.sidebar.markdown(encabezado_sidebar(), unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.caption(t("sidebar.idioma"))
    selector_idioma(ubicacion="sidebar")
    st.sidebar.markdown("---")
    st.sidebar.caption(t("sidebar.sesion"))

    nombre = st.session_state.get("usuario_actual")
    if not nombre and usuario:
        nombre = f"{usuario.nombres} {usuario.apellidos}"

    if nombre:
        st.sidebar.markdown(f"**{nombre}**")

    st.sidebar.markdown(
        f'<span class="role-badge">{t("sidebar.rol")}: {gestor.traducir_rol(rol)}</span>',
        unsafe_allow_html=True,
    )
    st.sidebar.caption(f"{t('sidebar.periodo')}: {sistema.periodo_actual or '—'}")

    if not st.session_state.get("db_cargada"):
        st.sidebar.warning(t("sidebar.demo"))

    if st.sidebar.button(t("sidebar.cerrar"), use_container_width=True):
        cerrar_sesion()


def main():
    page_icon = str(RUTA_LOGO) if RUTA_LOGO.exists() else "🎓"
    st.set_page_config(
        page_title=TITULO_APP,
        page_icon=page_icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )

    from interfaz.state import get_sistema
    from interfaz.styles import aplicar_estilos, pie_pagina

    aplicar_estilos()
    inicializar_sesion()

    sistema = get_sistema()

    if not esta_autenticado():
        pantalla_login(sistema)
        pie_pagina()
        return

    rol = obtener_rol_actual()
    usuario = obtener_usuario_actual(sistema)
    gestor = obtener_gestor_idioma()

    with st.sidebar:
        _render_sidebar_sesion(sistema, rol, usuario)
        st.markdown("---")
        st.caption(t("sidebar.menu"))

        opciones_internas = obtener_opciones_por_rol(rol)
        etiquetas = obtener_etiquetas_menu(rol)

        if st.session_state.nav_seleccion not in opciones_internas:
            st.session_state.nav_seleccion = dashboard_inicial_por_rol(rol)

        indice = opciones_internas.index(st.session_state.nav_seleccion)
        etiqueta_sel = st.radio(
            "Navegacion",
            etiquetas,
            index=indice,
            label_visibility="collapsed",
        )
        st.session_state.nav_seleccion = gestor.clave_menu(etiqueta_sel)

    opcion = st.session_state.nav_seleccion

    if not es_opcion_permitida(rol, opcion):
        st.error(t("app.sin_permisos"))
    elif opcion in RUTAS:
        RUTAS[opcion](sistema)
    else:
        st.error(t("app.sin_permisos"))

    pie_pagina()


main()
