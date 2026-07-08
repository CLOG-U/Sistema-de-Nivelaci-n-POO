import streamlit as st

from interfaz.branding import encabezado_pagina
from interfaz.components.forms import campos_usuario_base
from interfaz.components.layout import detalle_entidad, fila_metricas, intro_modulo, tabla_o_vacio
from interfaz.components.tables import usuario_detalle_campos, usuario_to_dict


def _formulario_estudiante(sistema):
    with st.form("form_estudiante"):
        datos = campos_usuario_base("est")
        tipo_documento = st.selectbox("Tipo de documento", ["Cedula", "Pasaporte"])
        fecha_nacimiento = st.text_input("Fecha de nacimiento (AAAA-MM-DD)")
        discapacidad = st.checkbox("Discapacidad")
        enviado = st.form_submit_button("Registrar estudiante", use_container_width=True)

    if enviado:
        try:
            if not all(
                [
                    datos["cedula"],
                    datos["nombres"],
                    datos["apellidos"],
                    datos["correo"],
                    datos["contrasena"],
                    datos["telefono"],
                    fecha_nacimiento,
                ]
            ):
                raise ValueError("Complete todos los campos obligatorios")

            estudiante = sistema.registrar_usuario(
                "Estudiante",
                datos["cedula"].strip(),
                datos["nombres"].strip(),
                datos["apellidos"].strip(),
                datos["correo"].strip(),
                datos["contrasena"].strip(),
                datos["telefono"].strip(),
                tipo_documento=tipo_documento,
                fecha_nacimiento=fecha_nacimiento.strip(),
                discapacidad=discapacidad,
            )
            st.success(
                f"Estudiante registrado: {estudiante.nombres} {estudiante.apellidos}. "
                f"Estado de nivelacion: {estudiante.estado_nivelacion}"
            )
        except Exception as error:
            st.error(str(error))


def _formulario_docente(sistema):
    with st.form("form_docente"):
        datos = campos_usuario_base("doc")
        titulo_profesional = st.text_input("Titulo profesional")
        especialidad = st.text_input("Especialidad")
        enviado = st.form_submit_button("Registrar docente", use_container_width=True)

    if enviado:
        try:
            if not all(
                [
                    datos["cedula"],
                    datos["nombres"],
                    datos["apellidos"],
                    datos["correo"],
                    datos["contrasena"],
                    datos["telefono"],
                    titulo_profesional,
                    especialidad,
                ]
            ):
                raise ValueError("Complete todos los campos obligatorios")

            docente = sistema.registrar_usuario(
                "Docente",
                datos["cedula"].strip(),
                datos["nombres"].strip(),
                datos["apellidos"].strip(),
                datos["correo"].strip(),
                datos["contrasena"].strip(),
                datos["telefono"].strip(),
                titulo_profesional=titulo_profesional.strip(),
                especialidad=especialidad.strip(),
            )
            st.success(f"Docente registrado: {docente.nombres} {docente.apellidos}")
        except Exception as error:
            st.error(str(error))


def _formulario_administrador(sistema):
    with st.form("form_administrador"):
        datos = campos_usuario_base("adm")
        cargo = st.text_input("Cargo")
        enviado = st.form_submit_button("Registrar administrador", use_container_width=True)

    if enviado:
        try:
            if not all(
                [
                    datos["cedula"],
                    datos["nombres"],
                    datos["apellidos"],
                    datos["correo"],
                    datos["contrasena"],
                    datos["telefono"],
                    cargo,
                ]
            ):
                raise ValueError("Complete todos los campos obligatorios")

            administrador = sistema.registrar_usuario(
                "Administrador",
                datos["cedula"].strip(),
                datos["nombres"].strip(),
                datos["apellidos"].strip(),
                datos["correo"].strip(),
                datos["contrasena"].strip(),
                datos["telefono"].strip(),
                cargo=cargo.strip(),
            )
            st.success(f"Administrador registrado: {administrador.nombres} {administrador.apellidos}")
        except Exception as error:
            st.error(str(error))


def _resumen_usuarios(sistema):
    intro_modulo(
        "Control central de usuarios del sistema academico. Registre perfiles y consulte su estado.",
        "👥",
    )
    fila_metricas(
        [
            ("Total usuarios", len(sistema.usuarios)),
            ("Estudiantes", len(sistema.listar_estudiantes())),
            ("Docentes", len(sistema.listar_docentes())),
            ("Administradores", len(sistema.listar_administradores())),
        ]
    )

    activos = sum(1 for u in sistema.usuarios.values() if u.estado)
    inactivos = len(sistema.usuarios) - activos
    fila_metricas([("Activos", activos), ("Inactivos", inactivos)], columnas=2)


def _consulta_usuarios(sistema):
    usuarios = list(sistema.usuarios.values())
    if not usuarios:
        st.warning("No hay usuarios registrados.")
        return

    filtro = st.selectbox(
        "Filtrar por tipo",
        ["Todos", "Estudiante", "Docente", "Administrador"],
    )

    if filtro != "Todos":
        usuarios = [u for u in usuarios if usuario_to_dict(u)["Tipo"] == filtro]

    busqueda = st.text_input("Buscar por cedula, nombre o correo").strip().lower()
    if busqueda:
        usuarios = [
            u
            for u in usuarios
            if busqueda in u.cedula.lower()
            or busqueda in u.nombres.lower()
            or busqueda in u.apellidos.lower()
            or busqueda in u.correo.lower()
        ]

    filas = [usuario_to_dict(usuario) for usuario in usuarios]
    if not tabla_o_vacio(filas, "No hay usuarios que coincidan con el filtro."):
        return

    st.markdown("#### Detalle de usuarios")
    for usuario in usuarios:
        titulo = f"{usuario.nombres} {usuario.apellidos} · {usuario.cedula}"
        detalle_entidad(titulo, usuario_detalle_campos(usuario))


def mostrar_usuarios(sistema):
    encabezado_pagina("Gestion de usuarios")

    tab_resumen, tab_registrar, tab_consulta = st.tabs(["Resumen", "Registrar", "Consulta"])

    with tab_resumen:
        _resumen_usuarios(sistema)

    with tab_registrar:
        intro_modulo("Formularios de registro por tipo de usuario.", "📝")
        with st.expander("Registrar estudiante", expanded=True):
            _formulario_estudiante(sistema)
        with st.expander("Registrar docente"):
            _formulario_docente(sistema)
        with st.expander("Registrar administrador"):
            _formulario_administrador(sistema)

    with tab_consulta:
        _consulta_usuarios(sistema)
