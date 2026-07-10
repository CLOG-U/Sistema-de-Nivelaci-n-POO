import base64

import streamlit as st

from interfaz.branding import (
    COLOR_BLANCO,
    COLOR_ROJO,
    NOMBRE_SISTEMA,
    RUTA_LOGO,
    RUTA_LOGO_VERTICAL,
    SIGLAS,
    UNIVERSIDAD,
)
from modelos.admin import Administrador
from modelos.docente import Docente
from modelos.estudiante import Estudiante


def inicializar_sesion():
    if "autenticado" not in st.session_state:
        st.session_state.autenticado = False
    if "rol_actual" not in st.session_state:
        st.session_state.rol_actual = None
    if "usuario_actual_id" not in st.session_state:
        st.session_state.usuario_actual_id = None
    if "usuario_actual" not in st.session_state:
        st.session_state.usuario_actual = None
    if "nav_seleccion" not in st.session_state:
        st.session_state.nav_seleccion = None


def cerrar_sesion():
    st.session_state.autenticado = False
    st.session_state.rol_actual = None
    st.session_state.usuario_actual_id = None
    st.session_state.usuario_actual = None
    st.session_state.nav_seleccion = None
    st.rerun()


def esta_autenticado():
    return bool(st.session_state.get("autenticado") and st.session_state.get("rol_actual"))


def obtener_rol_actual():
    return st.session_state.get("rol_actual")


def obtener_usuario_actual(sistema):
    if not esta_autenticado():
        return None

    usuario_id = st.session_state.get("usuario_actual_id")
    if usuario_id is None:
        return None

    return sistema.usuarios.get(usuario_id)


def _rol_desde_usuario(usuario):
    if isinstance(usuario, Administrador):
        return "Administrador"
    if isinstance(usuario, Docente):
        return "Docente"
    if isinstance(usuario, Estudiante):
        return "Estudiante"
    return None


def _dashboard_por_rol(rol):
    return {
        "Administrador": "Dashboard",
        "Docente": "Dashboard Docente",
        "Estudiante": "Dashboard Estudiante",
    }.get(rol)


def autenticar_usuario(sistema, identificador, contrasena):
    usuario = sistema.buscar_usuario_por_identificador(identificador)
    if not usuario:
        return False, "Usuario no encontrado. Verifique su usuario institucional."

    if not usuario.iniciar_sesion(contrasena):
        return False, "Contrasena incorrecta o usuario inactivo."

    rol = _rol_desde_usuario(usuario)
    if not rol:
        return False, "Tipo de usuario no reconocido en el sistema."

    nombre_completo = f"{usuario.nombres} {usuario.apellidos}"
    st.session_state.autenticado = True
    st.session_state.rol_actual = rol
    st.session_state.usuario_actual_id = usuario.id_usuario
    st.session_state.usuario_actual = nombre_completo
    st.session_state.nav_seleccion = _dashboard_por_rol(rol)
    return True, f"Bienvenido, {nombre_completo}"


def _logo_base64(ruta):
    if not ruta.exists():
        return None
    mime = "image/png" if ruta.suffix.lower() == ".png" else "image/jpeg"
    contenido = base64.b64encode(ruta.read_bytes()).decode()
    return f"data:{mime};base64,{contenido}"


def barra_superior_login():
    logo_src = _logo_base64(RUTA_LOGO)
    logo_html = (
        f'<img src="{logo_src}" alt="{SIGLAS}" class="uleam-topbar-logo-img" />'
        if logo_src
        else f'<span class="uleam-topbar-siglas">{SIGLAS}</span>'
    )
    return f"""
    <div class="uleam-topbar">
        <div class="uleam-topbar-inner">
            <div class="uleam-topbar-brand">{logo_html}</div>
            <div class="uleam-topbar-actions">
                <span class="uleam-lang">ES</span>
                <span class="uleam-lang-sep">|</span>
                <span class="uleam-lang uleam-lang-muted">EN</span>
            </div>
        </div>
    </div>
    """


def pantalla_login(sistema):
    from interfaz.styles import aplicar_estilos_login

    aplicar_estilos_login()
    st.markdown(barra_superior_login(), unsafe_allow_html=True)

    if not st.session_state.get("db_cargada"):
        st.warning(
            st.session_state.get(
                "db_mensaje",
                "Modo demostracion en memoria. Configure SQL Server para persistencia real.",
            )
        )

    _, col_centro, _ = st.columns([1, 1.1, 1])

    with col_centro:
        st.markdown('<div class="login-card">', unsafe_allow_html=True)

        if RUTA_LOGO_VERTICAL.exists():
            st.image(str(RUTA_LOGO_VERTICAL), width=120)
        elif RUTA_LOGO.exists():
            st.image(str(RUTA_LOGO), width=220)

        st.markdown(
            f"""
            <div class="login-card-header">
                <h2 class="login-title">{NOMBRE_SISTEMA}</h2>
                <p class="login-subtitle">{SIGLAS} · {UNIVERSIDAD}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("form_login_institucional", clear_on_submit=False):
            usuario = st.text_input(
                "Usuario",
                placeholder="Cedula o correo @uleam.edu.ec",
            )
            contrasena = st.text_input("Contrasena", type="password", placeholder="Ingrese su contrasena")
            enviar = st.form_submit_button("Acceder", use_container_width=True, type="primary")

            if enviar:
                if not usuario.strip() or not contrasena:
                    st.error("Complete usuario y contrasena.")
                else:
                    ok, mensaje = autenticar_usuario(sistema, usuario, contrasena)
                    if ok:
                        st.rerun()
                    else:
                        st.error(mensaje)

        st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("Credenciales de demostracion"):
            st.markdown(
                """
                | Rol | Usuario (cedula) | Contrasena |
                |-----|------------------|------------|
                | Administrador | 1300004444 | adm123 |
                | Docente | 1300001111 | doc123 |
                | Estudiante | 1300002222 | est123 |
                """
            )


def pantalla_seleccion_rol(sistema):
    pantalla_login(sistema)
