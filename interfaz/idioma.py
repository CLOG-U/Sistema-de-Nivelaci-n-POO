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
    "Importar Datos": {"es": "Importar Datos", "en": "Import Data"},
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
    "Mis Reportes": {"es": "Mis Reportes", "en": "My Reports"},
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
        "modulos.admin.importar": "Carga masiva de datasets universitarios desde CSV",
        "modulos.docente.cursos": "Consulta de cursos asignados al docente",
        "modulos.docente.horarios": "Horarios de los cursos del docente",
        "modulos.docente.estudiantes": "Listado, notas y asistencia de estudiantes",
        "modulos.docente.reportes": "Resumen academico de sus cursos",
        "modulos.estudiante.cursos": "Cursos en los que esta inscrito",
        "modulos.estudiante.horario": "Horario de clases personal",
        "modulos.estudiante.carga": "Asignaturas y creditos del periodo",
        "modulos.estudiante.perfil": "Datos personales, calificaciones y asistencia",
        "modulos.estudiante.reportes": "Descarga de reportes academicos personales",
        "layout.ir_a": "Ir a {nombre}",
        "dashboard.periodo_activo": "Periodo activo",
        "dashboard.estado_periodo": "Estado periodo",
        "dashboard.periodos_registrados": "Periodos registrados",
        "dashboard.usuarios": "Usuarios",
        "dashboard.docentes": "Docentes",
        "dashboard.estudiantes": "Estudiantes",
        "dashboard.cursos": "Cursos",
        "dashboard.aulas": "Aulas",
        "dashboard.inscripciones": "Inscripciones",
        "dashboard.calificaciones": "Calificaciones",
        "dashboard.asistencias": "Asistencias",
        "dashboard.cargas_academicas": "Cargas academicas",
        "dashboard.reportes": "Reportes",
        "dashboard.matriculas": "Matriculas",
        "dashboard.periodo": "Periodo",
        "dashboard.estado": "Estado",
        "dashboard.admin.titulo": "Panel de administracion academica",
        "dashboard.admin.sesion_activa": "Sesion activa: {nombre} · Rol: {rol}",
        "dashboard.admin.modo_admin": "Modo administracion · Periodo {periodo}",
        "dashboard.admin.intro": "**{sistema}** · Resumen general del periodo activo. Seleccione un modulo para ir directamente a su gestion.",
        "dashboard.admin.modulos_sistema": "Modulos del sistema",
        "dashboard.admin.cursos_activos": "Cursos activos del periodo",
        "dashboard.admin.sin_cursos": "No hay cursos registrados en el periodo actual.",
        "dashboard.admin.sin_cursos_tabla": "Sin cursos para mostrar.",
        "dashboard.docente.titulo": "Panel del docente",
        "dashboard.docente.bienvenido": "Bienvenido, {nombre}",
        "dashboard.docente.intro_resumen": "Resumen academico del docente en el periodo activo.",
        "dashboard.docente.no_docente": "No se encontro un docente seleccionado.",
        "dashboard.docente.cursos_asignados": "Cursos asignados",
        "dashboard.docente.titulo_profesional": "Titulo",
        "dashboard.docente.especialidad": "Especialidad",
        "dashboard.docente.tab_resumen": "Resumen",
        "dashboard.docente.tab_consulta": "Consulta",
        "dashboard.docente.accesos_rapidos": "Accesos rapidos",
        "dashboard.docente.sin_cursos": "Este docente no tiene cursos asignados.",
        "dashboard.docente.calificaciones_registradas": "Calificaciones registradas",
        "dashboard.docente.sin_calificaciones": "Sin calificaciones registradas.",
        "dashboard.estudiante.titulo": "Panel del estudiante",
        "dashboard.estudiante.bienvenido": "Bienvenido, {nombre}",
        "dashboard.estudiante.intro_resumen": "Resumen personal del estudiante en el periodo activo.",
        "dashboard.estudiante.no_estudiante": "No se encontro un estudiante seleccionado.",
        "dashboard.estudiante.cursos_inscritos": "Cursos inscritos",
        "dashboard.estudiante.estado_nivelacion": "Estado nivelacion",
        "dashboard.estudiante.accesos_rapidos": "Accesos rapidos",
        "dashboard.estudiante.mis_cursos": "Mis cursos",
        "dashboard.estudiante.mi_carga": "Mi carga academica",
        "dashboard.estudiante.mis_calificaciones": "Mis calificaciones",
        "dashboard.estudiante.mi_asistencia": "Mi asistencia",
        "dashboard.estudiante.sin_cursos": "Todavia no tienes cursos inscritos.",
        "dashboard.estudiante.sin_carga": "Sin carga academica generada.",
        "dashboard.estudiante.sin_calificaciones": "Sin calificaciones registradas.",
        "dashboard.estudiante.sin_asistencia": "Sin registros de asistencia.",
        "import.titulo": "Importacion de datos CSV",
        "import.tab_guia": "Guia",
        "import.tab_importar": "Importar",
        "import.intro_guia": "Guia para cargar datasets de la universidad respetando el orden de dependencias entre entidades.",
        "import.intro_importar": "Seleccione el tipo de datos, descargue la plantilla y suba su archivo CSV.",
        "import.orden_recomendado": "Importe en este orden: periodos → docentes/estudiantes/administradores → aulas → horarios → cursos → matriculas → cargas → calificaciones → asistencias.",
        "import.sin_tipos": "No hay tipos configurados.",
        "import.notas_titulo": "Notas importantes",
        "import.nota_persistencia": "- Los registros se guardan mediante los metodos del sistema (memoria y SQL si la BD esta activa).",
        "import.nota_referencias": "- Use cedulas y codigos existentes para vincular docentes, estudiantes, aulas, horarios y cursos.",
        "import.nota_duplicados": "- Filas con errores se omiten y se reportan al final; las demas se importan normalmente.",
        "import.seleccion_tipo": "Tipo de datos a importar",
        "import.columnas_requeridas": "Columnas requeridas",
        "import.columnas_opcionales": "Columnas opcionales",
        "import.descargar_plantilla": "Descargar plantilla CSV",
        "import.subir_csv": "Subir archivo CSV",
        "import.archivo_vacio": "El archivo no contiene filas validas.",
        "import.vista_previa": "Vista previa",
        "import.ejecutar": "Importar datos",
        "import.resultado_ok": "Importacion completada: {importadas} de {total} filas procesadas correctamente.",
        "import.resultado_vacio": "No se importo ningun registro.",
        "import.resultado_omitidas": "{omitidas} filas omitidas por errores.",
        "import.errores_titulo": "Detalle de errores",
        "import.solo_admin": "Solo un administrador puede importar datos.",
        "import.modo_demo": "Modo demo activo: los datos importados permanecen en memoria hasta conectar SQL Server.",
        "import.tipo.periodos": "Periodos academicos",
        "import.tipo.docentes": "Docentes",
        "import.tipo.estudiantes": "Estudiantes",
        "import.tipo.administradores": "Administradores",
        "import.tipo.aulas": "Aulas",
        "import.tipo.horarios": "Horarios",
        "import.tipo.cursos": "Cursos",
        "import.tipo.matriculas": "Matriculas / inscripciones",
        "import.tipo.cargas_academicas": "Cargas academicas",
        "import.tipo.calificaciones": "Calificaciones",
        "import.tipo.asistencias": "Asistencias",
        "import.desc.periodos": "Periodos academicos del sistema",
        "import.desc.docentes": "Docentes de la universidad",
        "import.desc.estudiantes": "Estudiantes de nivelacion",
        "import.desc.administradores": "Administradores del sistema",
        "import.desc.aulas": "Aulas y espacios fisicos",
        "import.desc.horarios": "Bloques horarios vinculados a aulas",
        "import.desc.cursos": "Cursos de nivelacion",
        "import.desc.matriculas": "Inscripciones de estudiantes en cursos",
        "import.desc.cargas_academicas": "Cargas academicas por estudiante y periodo",
        "import.desc.calificaciones": "Notas parciales por estudiante y curso",
        "import.desc.asistencias": "Registro de asistencia",
        "import.intro_guia_unificado": "Guia del modelo CSV unificado acoplado al importador del sistema.",
        "import.intro_importar_unificado": "Descargue la plantilla, complete el dataset con columna tipo_registro y suba un unico archivo CSV.",
        "import.orden_recomendado_unificado": "El importador procesa automaticamente las filas en orden: periodo, docente, estudiante, administrador, aula, horario, curso, matricula, carga_academica, calificacion, asistencia.",
        "import.subir_csv_unificado": "Subir dataset CSV unificado",
        "import.ejecutar_dataset": "Importar dataset completo",
        "import.resultado_dataset_ok": "Dataset importado: {importadas} de {total} filas procesadas correctamente.",
        "import.resultado_dataset_parcial": "Importacion parcial: {importadas} de {total} filas procesadas.",
        "import.resumen_fases": "Resumen por fase",
        "import.conteo_tipos": "Registros por tipo_registro",
        "import.importando": "Importando dataset...",
        "import.errores_mas": "Y {extra} errores adicionales.",
        "import.tipo.periodo": "Periodo academico",
        "import.tipo.docente": "Docente",
        "import.tipo.estudiante": "Estudiante",
        "import.tipo.administrador": "Administrador",
        "import.tipo.aula": "Aula",
        "import.tipo.horario": "Horario",
        "import.tipo.curso": "Curso",
        "import.tipo.matricula": "Matricula",
        "import.tipo.carga_academica": "Carga academica",
        "import.tipo.calificacion": "Calificacion",
        "import.tipo.asistencia": "Asistencia",
        "import.desc.periodo": "Periodos academicos del sistema",
        "import.desc.docente": "Docentes de la universidad",
        "import.desc.estudiante": "Estudiantes de nivelacion",
        "import.desc.administrador": "Administradores del sistema",
        "import.desc.aula": "Aulas y espacios fisicos",
        "import.desc.horario": "Bloques horarios vinculados a aulas",
        "import.desc.curso": "Cursos de nivelacion",
        "import.desc.matricula": "Inscripciones de estudiantes en cursos",
        "import.desc.carga_academica": "Cargas academicas por estudiante y periodo",
        "import.desc.calificacion": "Notas parciales por estudiante y curso",
        "import.desc.asistencia": "Registro de asistencia",
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
        "modulos.admin.importar": "Bulk import university datasets from CSV",
        "modulos.docente.cursos": "View courses assigned to the teacher",
        "modulos.docente.horarios": "Schedules for teacher courses",
        "modulos.docente.estudiantes": "Students, grades and attendance",
        "modulos.docente.reportes": "Academic summary of your courses",
        "modulos.estudiante.cursos": "Courses you are enrolled in",
        "modulos.estudiante.horario": "Personal class schedule",
        "modulos.estudiante.carga": "Subjects and credits for the term",
        "modulos.estudiante.perfil": "Personal data, grades and attendance",
        "modulos.estudiante.reportes": "Download personal academic reports",
        "layout.ir_a": "Go to {nombre}",
        "dashboard.periodo_activo": "Active term",
        "dashboard.estado_periodo": "Term status",
        "dashboard.periodos_registrados": "Registered terms",
        "dashboard.usuarios": "Users",
        "dashboard.docentes": "Teachers",
        "dashboard.estudiantes": "Students",
        "dashboard.cursos": "Courses",
        "dashboard.aulas": "Classrooms",
        "dashboard.inscripciones": "Enrollments",
        "dashboard.calificaciones": "Grades",
        "dashboard.asistencias": "Attendance",
        "dashboard.cargas_academicas": "Academic loads",
        "dashboard.reportes": "Reports",
        "dashboard.matriculas": "Registrations",
        "dashboard.periodo": "Term",
        "dashboard.estado": "Status",
        "dashboard.admin.titulo": "Academic administration panel",
        "dashboard.admin.sesion_activa": "Active session: {nombre} · Role: {rol}",
        "dashboard.admin.modo_admin": "Administration mode · Term {periodo}",
        "dashboard.admin.intro": "**{sistema}** · Overview of the active term. Select a module to go directly to its management.",
        "dashboard.admin.modulos_sistema": "System modules",
        "dashboard.admin.cursos_activos": "Active courses for the term",
        "dashboard.admin.sin_cursos": "No courses registered for the current term.",
        "dashboard.admin.sin_cursos_tabla": "No courses to display.",
        "dashboard.docente.titulo": "Teacher panel",
        "dashboard.docente.bienvenido": "Welcome, {nombre}",
        "dashboard.docente.intro_resumen": "Teacher academic summary for the active term.",
        "dashboard.docente.no_docente": "No teacher profile found.",
        "dashboard.docente.cursos_asignados": "Assigned courses",
        "dashboard.docente.titulo_profesional": "Degree",
        "dashboard.docente.especialidad": "Specialty",
        "dashboard.docente.tab_resumen": "Summary",
        "dashboard.docente.tab_consulta": "Query",
        "dashboard.docente.accesos_rapidos": "Quick access",
        "dashboard.docente.sin_cursos": "This teacher has no assigned courses.",
        "dashboard.docente.calificaciones_registradas": "Registered grades",
        "dashboard.docente.sin_calificaciones": "No grades registered.",
        "dashboard.estudiante.titulo": "Student panel",
        "dashboard.estudiante.bienvenido": "Welcome, {nombre}",
        "dashboard.estudiante.intro_resumen": "Personal student summary for the active term.",
        "dashboard.estudiante.no_estudiante": "No student profile found.",
        "dashboard.estudiante.cursos_inscritos": "Enrolled courses",
        "dashboard.estudiante.estado_nivelacion": "Leveling status",
        "dashboard.estudiante.accesos_rapidos": "Quick access",
        "dashboard.estudiante.mis_cursos": "My courses",
        "dashboard.estudiante.mi_carga": "My academic load",
        "dashboard.estudiante.mis_calificaciones": "My grades",
        "dashboard.estudiante.mi_asistencia": "My attendance",
        "dashboard.estudiante.sin_cursos": "You are not enrolled in any courses yet.",
        "dashboard.estudiante.sin_carga": "No academic load generated.",
        "dashboard.estudiante.sin_calificaciones": "No grades registered.",
        "dashboard.estudiante.sin_asistencia": "No attendance records.",
        "import.titulo": "CSV data import",
        "import.tab_guia": "Guide",
        "import.tab_importar": "Import",
        "import.intro_guia": "Guide to load university datasets following entity dependency order.",
        "import.intro_importar": "Select the data type, download the template and upload your CSV file.",
        "import.orden_recomendado": "Import in this order: terms → teachers/students/admins → classrooms → schedules → courses → enrollments → loads → grades → attendance.",
        "import.sin_tipos": "No types configured.",
        "import.notas_titulo": "Important notes",
        "import.nota_persistencia": "- Records are saved through system methods (memory and SQL when DB is active).",
        "import.nota_referencias": "- Use existing IDs and codes to link teachers, students, classrooms, schedules and courses.",
        "import.nota_duplicados": "- Rows with errors are skipped and reported; the rest are imported normally.",
        "import.seleccion_tipo": "Data type to import",
        "import.columnas_requeridas": "Required columns",
        "import.columnas_opcionales": "Optional columns",
        "import.descargar_plantilla": "Download CSV template",
        "import.subir_csv": "Upload CSV file",
        "import.archivo_vacio": "The file contains no valid rows.",
        "import.vista_previa": "Preview",
        "import.ejecutar": "Import data",
        "import.resultado_ok": "Import completed: {importadas} of {total} rows processed successfully.",
        "import.resultado_vacio": "No records were imported.",
        "import.resultado_omitidas": "{omitidas} rows skipped due to errors.",
        "import.errores_titulo": "Error details",
        "import.solo_admin": "Only an administrator can import data.",
        "import.modo_demo": "Demo mode active: imported data stays in memory until SQL Server is connected.",
        "import.tipo.periodos": "Academic terms",
        "import.tipo.docentes": "Teachers",
        "import.tipo.estudiantes": "Students",
        "import.tipo.administradores": "Administrators",
        "import.tipo.aulas": "Classrooms",
        "import.tipo.horarios": "Schedules",
        "import.tipo.cursos": "Courses",
        "import.tipo.matriculas": "Enrollments",
        "import.tipo.cargas_academicas": "Academic loads",
        "import.tipo.calificaciones": "Grades",
        "import.tipo.asistencias": "Attendance",
        "import.desc.periodos": "Academic terms in the system",
        "import.desc.docentes": "University teachers",
        "import.desc.estudiantes": "Leveling students",
        "import.desc.administradores": "System administrators",
        "import.desc.aulas": "Classrooms and physical spaces",
        "import.desc.horarios": "Schedule blocks linked to classrooms",
        "import.desc.cursos": "Leveling courses",
        "import.desc.matriculas": "Student course enrollments",
        "import.desc.cargas_academicas": "Academic load per student and term",
        "import.desc.calificaciones": "Partial grades per student and course",
        "import.desc.asistencias": "Attendance records",
        "import.intro_guia_unificado": "Guide for the unified CSV model coupled to the system importer.",
        "import.intro_importar_unificado": "Download the template, fill the dataset with tipo_registro column and upload a single CSV file.",
        "import.orden_recomendado_unificado": "The importer automatically processes rows in order: periodo, docente, estudiante, administrador, aula, horario, curso, matricula, carga_academica, calificacion, asistencia.",
        "import.subir_csv_unificado": "Upload unified CSV dataset",
        "import.ejecutar_dataset": "Import full dataset",
        "import.resultado_dataset_ok": "Dataset imported: {importadas} of {total} rows processed successfully.",
        "import.resultado_dataset_parcial": "Partial import: {importadas} of {total} rows processed.",
        "import.resumen_fases": "Summary by phase",
        "import.conteo_tipos": "Records by tipo_registro",
        "import.importando": "Importing dataset...",
        "import.errores_mas": "And {extra} additional errors.",
        "import.tipo.periodo": "Academic term",
        "import.tipo.docente": "Teacher",
        "import.tipo.estudiante": "Student",
        "import.tipo.administrador": "Administrator",
        "import.tipo.aula": "Classroom",
        "import.tipo.horario": "Schedule",
        "import.tipo.curso": "Course",
        "import.tipo.matricula": "Enrollment",
        "import.tipo.carga_academica": "Academic load",
        "import.tipo.calificacion": "Grade",
        "import.tipo.asistencia": "Attendance",
        "import.desc.periodo": "Academic terms in the system",
        "import.desc.docente": "University teachers",
        "import.desc.estudiante": "Leveling students",
        "import.desc.administrador": "System administrators",
        "import.desc.aula": "Classrooms and physical spaces",
        "import.desc.horario": "Schedule blocks linked to classrooms",
        "import.desc.curso": "Leveling courses",
        "import.desc.matricula": "Student course enrollments",
        "import.desc.carga_academica": "Academic load per student and term",
        "import.desc.calificacion": "Partial grades per student and course",
        "import.desc.asistencia": "Attendance records",
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
        # Asegura que el idioma esté inicializado en la sesión
        if "idioma" not in st.session_state:
            st.session_state.idioma = IDIOMA_DEFECTO

    def obtener_idioma(self) -> str:
        # Retorna el idioma actual, validando que sea válido
        self._asegurar_idioma_sesion()
        codigo = st.session_state.idioma
        return codigo if codigo in IDIOMAS_VALIDOS else IDIOMA_DEFECTO

    def cambiar_idioma(self, codigo: str):
        # Cambia el idioma si el código proporcionado es válido
        if codigo in IDIOMAS_VALIDOS:
            st.session_state.idioma = codigo

    def t(self, clave: str, **kwargs) -> str:
        # Traduce una clave al idioma actual con formato de parámetros opcionales
        idioma = self.obtener_idioma()
        texto = TRADUCCIONES.get(idioma, {}).get(clave)
        if texto is None:
            texto = TRADUCCIONES[IDIOMA_DEFECTO].get(clave, clave)
        return texto.format(**kwargs) if kwargs else texto

    def etiqueta_menu(self, clave_interna: str) -> str:
        # Convierte una clave interna de menú a su etiqueta visible en el idioma actual
        idioma = self.obtener_idioma()
        return MENU_INTERNO.get(clave_interna, {}).get(idioma, clave_interna)

    def clave_menu(self, etiqueta_visible: str) -> str:
        # Convierte una etiqueta visible de menú a su clave interna
        idioma = self.obtener_idioma()
        for clave, textos in MENU_INTERNO.items():
            if textos.get(idioma) == etiqueta_visible:
                return clave
        return etiqueta_visible

    def traducir_rol(self, rol: str) -> str:
        # Traduce un rol de usuario al idioma actual
        mapa = {
            "Administrador": "rol.administrador",
            "Docente": "rol.docente",
            "Estudiante": "rol.estudiante",
        }
        return self.t(mapa.get(rol, rol))


def obtener_gestor_idioma() -> GestorIdioma:
    # Retorna la instancia singleton del gestor de idioma
    return GestorIdioma()


def t(clave: str, **kwargs) -> str:
    # Función auxiliar para traducir una clave usando el gestor de idioma
    return obtener_gestor_idioma().t(clave, **kwargs)


def selector_idioma(ubicacion: str = "main"):
    # Renderiza botones de selección de idioma (ES | EN) en la ubicación especificada
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
