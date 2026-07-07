import streamlit as st

from interfaz.branding import encabezado_pagina
from interfaz.components.tables import horario_to_dict


def _formulario_horario(sistema):
    st.subheader("Registrar horario")

    if not sistema.aulas:
        st.warning("Debe registrar al menos un aula antes de crear un horario.")
        return

    opciones_aulas = {f"{aula.codigo} - {aula.nombre}": aula for aula in sistema.aulas}

    with st.form("form_horario"):
        dia = st.selectbox("Dia", ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"])
        hora_inicio = st.text_input("Hora inicio (HH:MM)")
        hora_fin = st.text_input("Hora fin (HH:MM)")
        modalidad = st.selectbox("Modalidad", ["Presencial", "Virtual", "Hibrida"])
        grupo = st.text_input("Grupo")
        aula_etiqueta = st.selectbox("Aula", list(opciones_aulas.keys()))

        enviado = st.form_submit_button("Registrar horario")

    if enviado:
        try:
            if not all([hora_inicio, hora_fin, grupo]):
                raise ValueError("Complete todos los campos obligatorios")

            aula = opciones_aulas[aula_etiqueta]
            horario = sistema.registrar_horario(
                dia,
                hora_inicio.strip(),
                hora_fin.strip(),
                modalidad,
                grupo.strip(),
                aula,
            )
            st.success(f"Horario registrado: {horario.dia} {horario.hora_inicio} - {horario.hora_fin}")
        except Exception as error:
            st.error(str(error))


def mostrar_horarios(sistema):
    encabezado_pagina("Gestion de horarios")

    _formulario_horario(sistema)

    st.divider()
    st.subheader("Horarios registrados")

    if not sistema.horarios:
        st.warning("No hay horarios registrados.")
        return

    filas = [horario_to_dict(horario) for horario in sistema.horarios]
    st.dataframe(filas, use_container_width=True, hide_index=True)
