import streamlit as st

from interfaz.components.tables import usuario_to_dict


def _formulario_estudiante(sistema):
    st.subheader("Registrar estudiante")

    with st.form("form_estudiante"):
        cedula = st.text_input("Cedula")
        nombres = st.text_input("Nombres")
        apellidos = st.text_input("Apellidos")
        correo = st.text_input("Correo")
        contrasena = st.text_input("Contrasena", type="password")
        telefono = st.text_input("Telefono")
        tipo_documento = st.selectbox("Tipo de documento", ["Cedula", "Pasaporte"])
        fecha_nacimiento = st.text_input("Fecha de nacimiento (AAAA-MM-DD)")
        discapacidad = st.checkbox("Discapacidad")

        enviado = st.form_submit_button("Registrar estudiante")

    if enviado:
        try:
            if not all([cedula, nombres, apellidos, correo, contrasena, telefono, fecha_nacimiento]):
                raise ValueError("Complete todos los campos obligatorios")

            estudiante = sistema.registrar_usuario(
                "Estudiante",
                cedula.strip(),
                nombres.strip(),
                apellidos.strip(),
                correo.strip(),
                contrasena.strip(),
                telefono.strip(),
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
        cedula = st.text_input("Cedula", key="doc_cedula")
        nombres = st.text_input("Nombres", key="doc_nombres")
        apellidos = st.text_input("Apellidos", key="doc_apellidos")
        correo = st.text_input("Correo", key="doc_correo")
        contrasena = st.text_input("Contrasena", type="password", key="doc_contrasena")
        telefono = st.text_input("Telefono", key="doc_telefono")
        titulo_profesional = st.text_input("Titulo profesional")
        especialidad = st.text_input("Especialidad")

        enviado = st.form_submit_button("Registrar docente")

    if enviado:
        try:
            if not all([cedula, nombres, apellidos, correo, contrasena, telefono, titulo_profesional, especialidad]):
                raise ValueError("Complete todos los campos obligatorios")

            docente = sistema.registrar_usuario(
                "Docente",
                cedula.strip(),
                nombres.strip(),
                apellidos.strip(),
                correo.strip(),
                contrasena.strip(),
                telefono.strip(),
                titulo_profesional=titulo_profesional.strip(),
                especialidad=especialidad.strip(),
            )
            st.success(f"Docente registrado: {docente.nombres} {docente.apellidos}")
        except Exception as error:
            st.error(str(error))


def _formulario_administrador(sistema):
    st.subheader("Registrar administrador")

    with st.form("form_administrador"):
        cedula = st.text_input("Cedula", key="adm_cedula")
        nombres = st.text_input("Nombres", key="adm_nombres")
        apellidos = st.text_input("Apellidos", key="adm_apellidos")
        correo = st.text_input("Correo", key="adm_correo")
        contrasena = st.text_input("Contrasena", type="password", key="adm_contrasena")
        telefono = st.text_input("Telefono", key="adm_telefono")
        cargo = st.text_input("Cargo")

        enviado = st.form_submit_button("Registrar administrador")

    if enviado:
        try:
            if not all([cedula, nombres, apellidos, correo, contrasena, telefono, cargo]):
                raise ValueError("Complete todos los campos obligatorios")

            administrador = sistema.registrar_usuario(
                "Administrador",
                cedula.strip(),
                nombres.strip(),
                apellidos.strip(),
                correo.strip(),
                contrasena.strip(),
                telefono.strip(),
                cargo=cargo.strip(),
            )
            st.success(f"Administrador registrado: {administrador.nombres} {administrador.apellidos}")
        except Exception as error:
            st.error(str(error))


def mostrar_usuarios(sistema):
    st.title("Usuarios")

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
