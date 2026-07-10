import streamlit as st

from interfaz.idioma import obtener_gestor_idioma, t


def obtener_opciones_por_rol(rol):
    if rol == "Administrador":
        return [
            "Dashboard",
            "Usuarios",
            "Aulas",
            "Horarios",
            "Cursos",
            "Inscripciones",
            "Cargas",
            "Reportes",
            "Acerca del Sistema",
        ]

    if rol == "Docente":
        return [
            "Dashboard Docente",
            "Mis Cursos",
            "Mis Horarios",
            "Mis Estudiantes",
            "Reportes Docente",
            "Acerca del Sistema",
        ]

    if rol == "Estudiante":
        return [
            "Dashboard Estudiante",
            "Mis Cursos",
            "Mi Horario",
            "Mi Carga",
            "Mi Perfil",
            "Acerca del Sistema",
        ]

    return []


def obtener_etiquetas_menu(rol):
    gestor = obtener_gestor_idioma()
    return [gestor.etiqueta_menu(opcion) for opcion in obtener_opciones_por_rol(rol)]


def dashboard_inicial_por_rol(rol):
    opciones = obtener_opciones_por_rol(rol)
    return opciones[0] if opciones else None


def es_opcion_permitida(rol, opcion):
    return opcion in obtener_opciones_por_rol(rol)


def navegar_a(opcion):
    """Cambia la vista activa desde un boton del dashboard."""
    st.session_state.nav_seleccion = opcion
    st.rerun()


MODULOS_ADMIN = [
    ("Usuarios", "modulos.admin.usuarios"),
    ("Aulas", "modulos.admin.aulas"),
    ("Horarios", "modulos.admin.horarios"),
    ("Cursos", "modulos.admin.cursos"),
    ("Inscripciones", "modulos.admin.inscripciones"),
    ("Cargas", "modulos.admin.cargas"),
    ("Reportes", "modulos.admin.reportes"),
]

MODULOS_DOCENTE = [
    ("Mis Cursos", "modulos.docente.cursos"),
    ("Mis Horarios", "modulos.docente.horarios"),
    ("Mis Estudiantes", "modulos.docente.estudiantes"),
    ("Reportes Docente", "modulos.docente.reportes"),
]

MODULOS_ESTUDIANTE = [
    ("Mis Cursos", "modulos.estudiante.cursos"),
    ("Mi Horario", "modulos.estudiante.horario"),
    ("Mi Carga", "modulos.estudiante.carga"),
    ("Mi Perfil", "modulos.estudiante.perfil"),
]


def _modulos_traducidos(modulos):
    gestor = obtener_gestor_idioma()
    return [
        (clave, gestor.etiqueta_menu(clave), gestor.t(desc))
        for clave, desc in modulos
    ]


def modulos_admin_traducidos():
    return _modulos_traducidos(MODULOS_ADMIN)


def modulos_docente_traducidos():
    return _modulos_traducidos(MODULOS_DOCENTE)


def modulos_estudiante_traducidos():
    return _modulos_traducidos(MODULOS_ESTUDIANTE)
