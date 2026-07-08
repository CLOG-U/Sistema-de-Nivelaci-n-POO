import streamlit as st

from interfaz.branding import NOMBRE_SISTEMA, mostrar_logo_login, UNIVERSIDAD, SIGLAS
from modelos.admin import Administrador
from modelos.docente import Docente
from modelos.estudiante import Estudiante

ROLES = {
    "Administrador": {
        "clave": "admin",
        "icono": "🛡️",
        "descripcion": "Gestiona usuarios, cursos, aulas, horarios, inscripciones, cargas y reportes.",
    },
    "Docente": {
        "clave": "docente",
        "icono": "👨‍🏫",
        "descripcion": "Consulta sus cursos, horarios, estudiantes asignados y reportes academicos.",
    },
    "Estudiante": {
        "clave": "estudiante",
        "icono": "🎓",
        "descripcion": "Consulta su horario, cursos inscritos, carga academica y estado de nivelacion.",
    },
}


def inicializar_sesion():
    if "rol_actual" not in st.session_state:
        st.session_state.rol_actual = None
    if "usuario_actual_id" not in st.session_state:
        st.session_state.usuario_actual_id = None
    if "nav_seleccion" not in st.session_state:
        st.session_state.nav_seleccion = None


def cerrar_sesion():
    st.session_state.rol_actual = None
    st.session_state.usuario_actual_id = None
    st.session_state.nav_seleccion = None
    st.rerun()


def obtener_rol_actual():
    return st.session_state.get("rol_actual")


def obtener_usuario_actual(sistema):
    rol = obtener_rol_actual()
    usuario_id = st.session_state.get("usuario_actual_id")

    if not rol or usuario_id is None:
        return None

    return sistema.usuarios.get(usuario_id)


def usuarios_por_rol(sistema, rol):
    if rol == "Estudiante":
        return sistema.listar_estudiantes()

    if rol == "Docente":
        return sistema.listar_docentes()

    if rol == "Administrador":
        return [u for u in sistema.usuarios.values() if isinstance(u, Administrador)]

    return []


def _rol_desde_usuario(usuario):
    if isinstance(usuario, Administrador):
        return "Administrador"
    if isinstance(usuario, Docente):
        return "Docente"
    if isinstance(usuario, Estudiante):
        return "Estudiante"
    return None


def autenticar_usuario(sistema, identificador, contrasena):
    usuario = sistema.buscar_usuario_por_identificador(identificador)
    if not usuario:
        return False, "Usuario no encontrado. Verifique cedula o correo institucional."

    if not usuario.iniciar_sesion(contrasena):
        return False, "Contrasena incorrecta o usuario inactivo."

    rol = _rol_desde_usuario(usuario)
    if not rol:
        return False, "Tipo de usuario no reconocido en el sistema."

    st.session_state.rol_actual = rol
    st.session_state.usuario_actual_id = usuario.id_usuario
    st.session_state.nav_seleccion = None
    return True, f"Bienvenido, {usuario.nombres} {usuario.apellidos}"


def pantalla_login(sistema):
    col_izq, col_centro, col_der = st.columns([1, 2, 1])

    with col_centro:
        mostrar_logo_login()
        st.markdown(f"## {NOMBRE_SISTEMA}")
        st.markdown(f"**{SIGLAS}** · {UNIVERSIDAD}")
        st.caption("Ingrese con su cedula o correo institucional (@uleam.edu.ec).")

        with st.form("form_login", clear_on_submit=False):
            identificador = st.text_input(
                "Cedula o correo",
                placeholder="1300002222 o usuario@uleam.edu.ec",
            )
            contrasena = st.text_input("Contrasena", type="password")
            enviar = st.form_submit_button("Iniciar sesion", use_container_width=True)

            if enviar:
                if not identificador.strip() or not contrasena:
                    st.error("Complete cedula/correo y contrasena.")
                else:
                    ok, mensaje = autenticar_usuario(sistema, identificador, contrasena)
                    if ok:
                        st.success(mensaje)
                        st.rerun()
                    else:
                        st.error(mensaje)

        with st.expander("Credenciales de prueba (POOPROYECTO.sql)"):
            st.markdown(
                """
                | Rol | Cedula | Contrasena |
                |-----|--------|------------|
                | Administrador | 1300004444 | adm123 |
                | Docente | 1300001111 | doc123 |
                | Estudiante | 1300002222 | est123 |
                | Estudiante | 1300003333 | est456 |
                """
            )


def pantalla_seleccion_rol(sistema):
    """Mantiene compatibilidad; redirige al login real."""
    pantalla_login(sistema)
