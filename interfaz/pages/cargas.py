import streamlit as st

from interfaz.components.tables import carga_to_dict


def _formulario_carga(sistema):
    st.subheader("Registrar carga academica")

    estudiantes = sistema.listar_estudiantes()
    if not estudiantes:
        st.warning("No hay estudiantes registrados.")
        return

    opciones_estudiantes = {f"{e.cedula} - {e.nombres} {e.apellidos}": e for e in estudiantes}

    with st.form("form_carga"):
        estudiante_etiqueta = st.selectbox("Estudiante", list(opciones_estudiantes.keys()))
        enviado = st.form_submit_button("Generar carga academica")

    if enviado:
        try:
            estudiante = opciones_estudiantes[estudiante_etiqueta]
            carga = sistema.registrar_carga_academica(estudiante)
            st.success(
                f"Carga generada para {estudiante.nombres} {estudiante.apellidos}. "
                f"Periodo: {carga.periodo}. "
                f"Asignaturas: {carga.total_asignaturas}. "
                f"Creditos: {carga.total_creditos}."
            )
        except Exception as error:
            st.error(str(error))


def mostrar_cargas(sistema):
    st.title("Cargas Academicas")

    _formulario_carga(sistema)

    st.divider()
    st.subheader("Cargas academicas registradas")

    if not sistema.cargas_academicas:
        st.warning("No hay cargas academicas registradas.")
        return

    filas = [carga_to_dict(carga) for carga in sistema.cargas_academicas]
    st.dataframe(filas, use_container_width=True, hide_index=True)
