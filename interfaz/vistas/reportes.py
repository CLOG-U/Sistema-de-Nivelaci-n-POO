import streamlit as st

from interfaz.branding import encabezado_pagina
from interfaz.components.layout import detalle_entidad, fila_metricas, intro_modulo, tabla_o_vacio
from interfaz.components.tables import asistencia_registro_to_dict, calificacion_registro_to_dict, reporte_to_dict
from servicios.exportador_reportes import construir_datos_exportacion, exportar_reporte, obtener_filas_reporte


def _mostrar_descarga(archivo, etiqueta="Descargar archivo"):
    st.download_button(
        label=etiqueta,
        data=archivo.contenido,
        file_name=archivo.nombre,
        mime=archivo.mime,
        use_container_width=True,
        type="primary",
    )


def _formulario_reporte(sistema):
    periodos = sistema.listar_periodos()

    with st.form("form_reporte"):
        tipo_reporte = st.selectbox(
            "Tipo de reporte",
            ["Asistencia", "Calificaciones", "Inscripciones", "Carga academica", "General"],
        )
        periodo = st.selectbox("Periodo academico", periodos)
        descripcion = st.text_input("Descripcion", value="Reporte academico del periodo")
        formato = st.selectbox("Formato", ["PDF", "Excel"])
        enviado = st.form_submit_button("Generar reporte", use_container_width=True)

    if enviado:
        try:
            if not descripcion:
                raise ValueError("Complete todos los campos obligatorios")

            filas = obtener_filas_reporte(sistema, tipo_reporte, periodo)
            resumen_previo = sistema.resumen_datos_reporte(tipo_reporte, periodo)
            st.info(f"Datos reales incluidos: {resumen_previo}")

            reporte = sistema.generar_reporte(
                tipo_reporte,
                periodo,
                descripcion.strip(),
                formato,
            )
            reporte.generar_reporte()
            archivo = reporte.exportar(filas)

            st.session_state["ultimo_reporte_archivo"] = archivo
            st.session_state["ultimo_reporte_id"] = reporte.id_reporte
            st.success(f"Reporte generado en formato {reporte.formato}. Use el boton para descargarlo.")
        except Exception as error:
            st.error(str(error))

    if st.session_state.get("ultimo_reporte_archivo"):
        st.markdown("#### Descarga del ultimo reporte generado")
        _mostrar_descarga(st.session_state["ultimo_reporte_archivo"])


def _resumen_reportes(sistema):
    intro_modulo(
        "Reportes con datos reales de asistencia, calificaciones, inscripciones y cargas del periodo.",
        "📊",
    )
    reportes = list(sistema.reportes.values())
    pdf = sum(1 for r in reportes if r.formato == "PDF")
    excel = sum(1 for r in reportes if r.formato == "Excel")
    tipos = len({r.tipo_reporte for r in reportes})

    fila_metricas(
        [
            ("Reportes generados", len(reportes)),
            ("Calificaciones", len(sistema.calificaciones)),
            ("Asistencias", len(sistema.asistencias)),
            ("Tipos distintos", tipos),
        ]
    )
    fila_metricas(
        [
            ("Formato PDF", pdf),
            ("Formato Excel", excel),
            ("Periodo activo", sistema.periodo_actual),
        ],
        columnas=3,
    )

    if reportes:
        por_tipo = {}
        for reporte in reportes:
            por_tipo[reporte.tipo_reporte] = por_tipo.get(reporte.tipo_reporte, 0) + 1
        st.markdown("#### Reportes por tipo")
        st.bar_chart(por_tipo)


def _consulta_reportes(sistema):
    reportes = list(sistema.reportes.values())
    if not reportes:
        st.warning("No hay reportes generados.")
        return

    filtro_formato = st.selectbox("Filtrar por formato", ["Todos", "PDF", "Excel"])
    if filtro_formato != "Todos":
        reportes = [r for r in reportes if r.formato == filtro_formato]

    filas = [reporte_to_dict(reporte) for reporte in reportes]
    if not tabla_o_vacio(filas, "No hay reportes con ese filtro."):
        return

    for reporte in reportes:
        detalle_entidad(
            f"Reporte {reporte.id_reporte} · {reporte.tipo_reporte}",
            [
                ("Periodo", reporte.periodo),
                ("Fecha", reporte.fecha_generacion),
                ("Formato", reporte.formato),
                ("Descripcion", reporte.descripcion),
            ],
        )
        try:
            filas_reporte = obtener_filas_reporte(sistema, reporte.tipo_reporte, reporte.periodo)
            datos = construir_datos_exportacion(reporte, filas_reporte)
            archivo = exportar_reporte(datos, reporte.formato)
            _mostrar_descarga(
                archivo,
                etiqueta=f"Descargar {reporte.formato} · Reporte {reporte.id_reporte}",
            )
        except Exception as error:
            st.error(f"No se pudo preparar la descarga: {error}")

    st.markdown("#### Datos academicos usados en reportes")
    col1, col2 = st.columns(2)
    with col1:
        calificaciones = [
            calificacion_registro_to_dict(registro)
            for registro in sistema.calificaciones.values()
        ]
        st.markdown("**Calificaciones registradas**")
        tabla_o_vacio(calificaciones, "Sin calificaciones.")
    with col2:
        asistencias = [
            asistencia_registro_to_dict(registro) for registro in sistema.asistencias.values()
        ]
        st.markdown("**Asistencias registradas**")
        tabla_o_vacio(asistencias, "Sin asistencias.")


def mostrar_reportes(sistema):
    encabezado_pagina("Reportes academicos", periodo=sistema.periodo_actual)

    tab_resumen, tab_registrar, tab_consulta = st.tabs(["Resumen", "Registrar", "Consulta"])

    with tab_resumen:
        _resumen_reportes(sistema)

    with tab_registrar:
        intro_modulo("Genere reportes exportables con resumen de datos reales del periodo.", "📝")
        _formulario_reporte(sistema)

    with tab_consulta:
        _consulta_reportes(sistema)
