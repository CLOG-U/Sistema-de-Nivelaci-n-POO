import streamlit as st

from interfaz.components.tables import reporte_to_dict


def _formulario_reporte(sistema):
    st.subheader("Generar reporte")

    periodos = sistema.listar_periodos()

    with st.form("form_reporte"):
        tipo_reporte = st.text_input("Tipo de reporte", value="Asistencia")
        periodo = st.selectbox("Periodo", periodos)
        descripcion = st.text_input("Descripcion", value="Reporte academico")
        formato = st.selectbox("Formato", ["PDF", "Excel"])

        enviado = st.form_submit_button("Generar reporte")

    if enviado:
        try:
            if not tipo_reporte or not descripcion:
                raise ValueError("Complete todos los campos obligatorios")

            reporte = sistema.generar_reporte(
                tipo_reporte.strip(),
                periodo,
                descripcion.strip(),
                formato,
            )
            reporte.generar_reporte()
            reporte.exportar()
            st.success(f"Reporte generado en formato {reporte.formato}")
        except Exception as error:
            st.error(str(error))


def mostrar_reportes(sistema):
    st.title("Reportes")

    _formulario_reporte(sistema)

    st.divider()
    st.subheader("Reportes generados")

    if not sistema.reportes:
        st.warning("No hay reportes generados.")
        return

    filas = [reporte_to_dict(reporte) for reporte in sistema.reportes]
    st.dataframe(filas, use_container_width=True, hide_index=True)
