import streamlit as st


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
    ("Usuarios", "Gestion de estudiantes, docentes y administradores"),
    ("Aulas", "Registro y consulta de espacios fisicos"),
    ("Horarios", "Planificacion de dias, horas y modalidad"),
    ("Cursos", "Creacion de cursos de nivelacion"),
    ("Inscripciones", "Matricula de estudiantes en cursos"),
    ("Cargas", "Generacion de carga por periodo"),
    ("Reportes", "Exportacion PDF y Excel"),
]

MODULOS_DOCENTE = [
    ("Mis Cursos", "Consulta de cursos asignados al docente"),
    ("Mis Horarios", "Horarios de los cursos del docente"),
    ("Mis Estudiantes", "Listado, notas y asistencia de estudiantes"),
    ("Reportes Docente", "Resumen academico de sus cursos"),
]

MODULOS_ESTUDIANTE = [
    ("Mis Cursos", "Cursos en los que esta inscrito"),
    ("Mi Horario", "Horario de clases personal"),
    ("Mi Carga", "Asignaturas y creditos del periodo"),
    ("Mi Perfil", "Datos personales, calificaciones y asistencia"),
]
