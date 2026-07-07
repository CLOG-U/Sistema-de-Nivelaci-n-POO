import streamlit as st

from interfaz.branding import encabezado_pagina
from interfaz.components.forms import campos_usuario_base
from interfaz.components.tables import usuario_to_dict


def _formulario_estudiante(sistema):
    st.subheader("Registrar estudiante")

    with st.form("form_estudiante"):
        datos = campos_usuario_base("est")
        tipo_documento = st.selectbox("Tipo de documento", ["Cedula", "Pasaporte"])
        fecha_nacimiento = st.text_input("Fecha de nacimiento (AAAA-MM-DD)")
        discapacidad = st.checkbox("Discapacidad")
        enviado = st.form_submit_button("Registrar estudiante")

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
    st.subheader("Registrar docente")

    with st.form("form_docente"):
        datos = campos_usuario_base("doc")
        titulo_profesional = st.text_input("Titulo profesional")
        especialidad = st.text_input("Especialidad")
        enviado = st.form_submit_button("Registrar docente")

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
    st.subheader("Registrar administrador")

    with st.form("form_administrador"):
        datos = campos_usuario_base("adm")
        cargo = st.text_input("Cargo")
        enviado = st.form_submit_button("Registrar administrador")

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


def mostrar_usuarios(sistema):
    encabezado_pagina("Gestion de usuarios")

    _formulario_estudiante(sistema)
    st.divider()
    _formulario_docente(sistema)
    st.divider()
    _formulario_administrador(sistema)

    st.divider()
    st.subheader("Usuarios registrados")

    if not sistema.usuarios:
        st.warning("No hay usuarios registrados.")
        return

    filas = [usuario_to_dict(usuario) for usuario in sistema.usuarios]
    st.dataframe(filas, use_container_width=True, hide_index=True)
