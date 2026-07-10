"""Gestor de idioma (Singleton) para la interfaz Streamlit."""

import streamlit as st

IDIOMA_DEFECTO = "es"
IDIOMAS_VALIDOS = ("es", "en")

# Claves internas de menu (coinciden con RUTAS en app.py)
MENU_INTERNO = {
    "Dashboard": {"es": "Dashboard", "en": "Dashboard"},
    "Usuarios": {"es": "Usuarios", "en": "Users"},
    "Aulas": {"es": "Aulas", "en": "Classrooms"},
    "Horarios": {"es": "Horarios", "en": "Schedules"},
    "Cursos": {"es": "Cursos", "en": "Courses"},
    "Inscripciones": {"es": "Inscripciones", "en": "Enrollments"},
    "Cargas": {"es": "Cargas", "en": "Academic Loads"},
    "Reportes": {"es": "Reportes", "en": "Reports"},
    "Acerca del Sistema": {"es": "Acerca del Sistema", "en": "About"},
    "Dashboard Docente": {"es": "Dashboard Docente", "en": "Teacher Dashboard"},
    "Mis Cursos": {"es": "Mis Cursos", "en": "My Courses"},
    "Mis Horarios": {"es": "Mis Horarios", "en": "My Schedules"},
    "Mis Estudiantes": {"es": "Mis Estudiantes", "en": "My Students"},
    "Reportes Docente": {"es": "Reportes Docente", "en": "Teacher Reports"},
    "Dashboard Estudiante": {"es": "Dashboard Estudiante", "en": "Student Dashboard"},
    "Mi Horario": {"es": "Mi Horario", "en": "My Schedule"},
    "Mi Carga": {"es": "Mi Carga", "en": "My Load"},
    "Mi Perfil": {"es": "Mi Perfil", "en": "My Profile"},
}

TRADUCCIONES = {
    "es": {
        "app.titulo_sistema": "Sistema de Nivelacion Academica",
        "app.universidad": "Universidad Laica Eloy Alfaro de Manabi",
        "login.usuario": "Usuario",
        "login.contrasena": "Contrasena",
        "login.placeholder_usuario": "Cedula o correo @uleam.edu.ec",
        "login.placeholder_contrasena": "Ingrese su contrasena",
        "login.acceder": "Acceder",
        "login.error_campos": "Complete usuario y contrasena.",
        "login.error_usuario": "Usuario no encontrado. Verifique su usuario institucional.",
        "login.error_contrasena": "Contrasena incorrecta o usuario inactivo.",
        "login.error_rol": "Tipo de usuario no reconocido en el sistema.",
        "login.bienvenida": "Bienvenido, {nombre}",
        "login.credenciales_titulo": "Credenciales de demostracion",
        "login.tabla_rol": "Rol",
        "login.tabla_usuario": "Usuario (cedula)",
        "login.tabla_contrasena": "Contrasena",
        "sidebar.sesion": "Sesion activa",
        "sidebar.idioma": "Idioma",
        "sidebar.rol": "Rol",
        "sidebar.periodo": "Periodo",
        "sidebar.cerrar": "Cerrar sesion",
        "sidebar.menu": "Menu de navegacion",
        "sidebar.demo": "Modo demo en memoria.",
        "app.sin_permisos": "No tiene permisos para acceder a esta seccion.",
        "app.demo_sql": "Modo demostracion en memoria. Configure SQL Server para persistencia real.",
        "rol.administrador": "Administrador",
        "rol.docente": "Docente",
        "rol.estudiante": "Estudiante",
        "modulos.admin.usuarios": "Gestion de estudiantes, docentes y administradores",
        "modulos.admin.aulas": "Registro y consulta de espacios fisicos",
        "modulos.admin.horarios": "Planificacion de dias, horas y modalidad",
        "modulos.admin.cursos": "Creacion de cursos de nivelacion",
        "modulos.admin.inscripciones": "Matricula de estudiantes en cursos",
        "modulos.admin.cargas": "Generacion de carga por periodo",
        "modulos.admin.reportes": "Exportacion PDF y Excel",
        "modulos.docente.cursos": "Consulta de cursos asignados al docente",
        "modulos.docente.horarios": "Horarios de los cursos del docente",
        "modulos.docente.estudiantes": "Listado, notas y asistencia de estudiantes",
        "modulos.docente.reportes": "Resumen academico de sus cursos",
        "modulos.estudiante.cursos": "Cursos en los que esta inscrito",
        "modulos.estudiante.horario": "Horario de clases personal",
        "modulos.estudiante.carga": "Asignaturas y creditos del periodo",
        "modulos.estudiante.perfil": "Datos personales, calificaciones y asistencia",
        "layout.ir_a": "Ir a {nombre}",
    },
    "en": {
        "app.titulo_sistema": "Academic Leveling System",
        "app.universidad": "Eloy Alfaro Laic University of Manabi",
        "login.usuario": "Username",
        "login.contrasena": "Password",
        "login.placeholder_usuario": "ID or email @uleam.edu.ec",
        "login.placeholder_contrasena": "Enter your password",
        "login.acceder": "Sign in",
        "login.error_campos": "Please enter username and password.",
        "login.error_usuario": "User not found. Check your institutional credentials.",
        "login.error_contrasena": "Incorrect password or inactive user.",
        "login.error_rol": "Unrecognized user type in the system.",
        "login.bienvenida": "Welcome, {nombre}",
        "login.credenciales_titulo": "Demo credentials",
        "login.tabla_rol": "Role",
        "login.tabla_usuario": "User (ID)",
        "login.tabla_contrasena": "Password",
        "sidebar.sesion": "Active session",
        "sidebar.idioma": "Language",
        "sidebar.rol": "Role",
        "sidebar.periodo": "Term",
        "sidebar.cerrar": "Sign out",
        "sidebar.menu": "Navigation menu",
        "sidebar.demo": "In-memory demo mode.",
        "app.sin_permisos": "You do not have permission to access this section.",
        "app.demo_sql": "In-memory demo mode. Configure SQL Server for real persistence.",
        "rol.administrador": "Administrator",
        "rol.docente": "Teacher",
        "rol.estudiante": "Student",
        "modulos.admin.usuarios": "Manage students, teachers and administrators",
        "modulos.admin.aulas": "Register and view physical spaces",
        "modulos.admin.horarios": "Plan days, times and modality",
        "modulos.admin.cursos": "Create leveling courses",
        "modulos.admin.inscripciones": "Enroll students in courses",
        "modulos.admin.cargas": "Generate academic load by term",
        "modulos.admin.reportes": "Export PDF and Excel",
        "modulos.docente.cursos": "View courses assigned to the teacher",
        "modulos.docente.horarios": "Schedules for teacher courses",
        "modulos.docente.estudiantes": "Students, grades and attendance",
        "modulos.docente.reportes": "Academic summary of your courses",
        "modulos.estudiante.cursos": "Courses you are enrolled in",
        "modulos.estudiante.horario": "Personal class schedule",
        "modulos.estudiante.carga": "Subjects and credits for the term",
        "modulos.estudiante.perfil": "Personal data, grades and attendance",
        "layout.ir_a": "Go to {nombre}",
    },
}


class GestorIdioma:
    """Singleton: unica instancia de gestion de idioma por sesion de la app."""

    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        return cls._instancia

    def _asegurar_idioma_sesion(self):
        if "idioma" not in st.session_state:
            st.session_state.idioma = IDIOMA_DEFECTO

    def obtener_idioma(self) -> str:
        self._asegurar_idioma_sesion()
        codigo = st.session_state.idioma
        return codigo if codigo in IDIOMAS_VALIDOS else IDIOMA_DEFECTO

    def cambiar_idioma(self, codigo: str):
        if codigo in IDIOMAS_VALIDOS:
            st.session_state.idioma = codigo

    def t(self, clave: str, **kwargs) -> str:
        idioma = self.obtener_idioma()
        texto = TRADUCCIONES.get(idioma, {}).get(clave)
        if texto is None:
            texto = TRADUCCIONES[IDIOMA_DEFECTO].get(clave, clave)
        return texto.format(**kwargs) if kwargs else texto

    def etiqueta_menu(self, clave_interna: str) -> str:
        idioma = self.obtener_idioma()
        return MENU_INTERNO.get(clave_interna, {}).get(idioma, clave_interna)

    def clave_menu(self, etiqueta_visible: str) -> str:
        idioma = self.obtener_idioma()
        for clave, textos in MENU_INTERNO.items():
            if textos.get(idioma) == etiqueta_visible:
                return clave
        return etiqueta_visible

    def traducir_rol(self, rol: str) -> str:
        mapa = {
            "Administrador": "rol.administrador",
            "Docente": "rol.docente",
            "Estudiante": "rol.estudiante",
        }
        return self.t(mapa.get(rol, rol))


def obtener_gestor_idioma() -> GestorIdioma:
    return GestorIdioma()


def t(clave: str, **kwargs) -> str:
    return obtener_gestor_idioma().t(clave, **kwargs)


def selector_idioma(ubicacion: str = "main"):
    """Botones ES | EN. ubicacion: 'main' (login) o 'sidebar'."""
    gestor = obtener_gestor_idioma()
    idioma = gestor.obtener_idioma()

    if ubicacion == "sidebar":
        col_es, col_en = st.sidebar.columns(2)
    else:
        col_es, col_en = st.columns(2)

    with col_es:
        if st.button(
            "ES",
            key=f"lang_es_{ubicacion}",
            use_container_width=True,
            type="primary" if idioma == "es" else "secondary",
        ):
            gestor.cambiar_idioma("es")
            st.rerun()
    with col_en:
        if st.button(
            "EN",
            key=f"lang_en_{ubicacion}",
            use_container_width=True,
            type="primary" if idioma == "en" else "secondary",
        ):
            gestor.cambiar_idioma("en")
            st.rerun()
