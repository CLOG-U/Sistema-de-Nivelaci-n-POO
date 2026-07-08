import streamlit as st

from interfaz.branding import NOMBRE_SISTEMA

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
        from modelos.admin import Administrador

        return [u for u in sistema.usuarios.values() if isinstance(u, Administrador)]

    return []


def pantalla_seleccion_rol(sistema):
    st.markdown(f"## {NOMBRE_SISTEMA}")
    st.markdown("### Seleccione el tipo de perfil para ingresar a una experiencia personalizada.")
    st.caption("Esta version utiliza perfiles demo para representar el acceso por roles.")

    st.info(
        "El sistema utiliza una interfaz diferenciada por roles, permitiendo que administradores, "
        "docentes y estudiantes accedan unicamente a las funciones correspondientes a su perfil."
    )

    st.markdown("---")

    for rol, info in ROLES.items():
        with st.container(border=True):
            icono_col, texto_col, boton_col = st.columns([2, 5, 2])

            with icono_col:
                st.markdown(
                    f"<div class='role-icon-wrap'><span class='role-icon'>{info['icono']}</span></div>",
                    unsafe_allow_html=True,
                )

            with texto_col:
                st.markdown(f"### {rol}")
                st.markdown(f"<p class='role-desc'>{info['descripcion']}</p>", unsafe_allow_html=True)

            with boton_col:
                st.markdown("<div style='padding-top:12px;'></div>", unsafe_allow_html=True)
                if st.button(f"Entrar", key=f"btn_{rol}", use_container_width=True):
                    st.session_state.rol_actual = rol

                    usuarios = usuarios_por_rol(sistema, rol)
                    if usuarios:
                        st.session_state.usuario_actual_id = usuarios[0].id_usuario

                    st.rerun()

        st.markdown("")
