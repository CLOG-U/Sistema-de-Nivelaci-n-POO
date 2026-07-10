import streamlit as st


def campos_usuario_base(prefijo):
    # Crea campos de entrada para datos básicos del usuario con prefijo único
    cedula = st.text_input("Cedula", key=f"{prefijo}_cedula")
    nombres = st.text_input("Nombres", key=f"{prefijo}_nombres")
    apellidos = st.text_input("Apellidos", key=f"{prefijo}_apellidos")
    correo = st.text_input("Correo", key=f"{prefijo}_correo")
    contrasena = st.text_input("Contrasena", type="password", key=f"{prefijo}_contrasena")
    telefono = st.text_input("Telefono", key=f"{prefijo}_telefono")
    return {
        "cedula": cedula,
        "nombres": nombres,
        "apellidos": apellidos,
        "correo": correo,
        "contrasena": contrasena,
        "telefono": telefono,
    }
