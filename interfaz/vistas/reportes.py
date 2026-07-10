import streamlit as st

from interfaz.auth import obtener_rol_actual, obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.layout import fila_metricas, intro_modulo, tabla_o_vacio
from interfaz.components.reportes_ui import panel_generar_reporte
from interfaz.components.tables import reporte_to_dict
from servicios.exportador_reportes import (
    construir_datos_exportacion,
    exportar_reporte,
    obtener_filas_reporte,
    resumen_filas_reporte,
)


def _mostrar_descarga(archivo, etiqueta="Descargar archivo"):
    st.download_button(
        label=etiqueta,
        data=archivo.contenido,
        file_name=archivo.nombre,
        mime=archivo.mime,
        use_container_width=True,
        type="primary",
    )


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
        st.warning("No hay reportes generados previamente.")
        return

    filtro_formato = st.selectbox("Filtrar por formato", ["Todos", "PDF", "Excel"])
    if filtro_formato != "Todos":
        reportes = [r for r in reportes if r.formato == filtro_formato]

    filas = [reporte_to_dict(reporte) for reporte in reportes]
    if not tabla_o_vacio(filas, "No hay reportes con ese filtro."):
        return

    for reporte in reportes:
        with st.expander(f"Reporte {reporte.id_reporte} · {reporte.tipo_reporte} ({reporte.formato})"):
            st.write(f"**Periodo:** {reporte.periodo}")
            st.write(f"**Fecha:** {reporte.fecha_generacion}")
            st.write(f"**Descripcion:** {reporte.descripcion}")
            try:
                filas_reporte = obtener_filas_reporte(sistema, reporte.tipo_reporte, reporte.periodo)
                st.caption(resumen_filas_reporte(filas_reporte))
                datos = construir_datos_exportacion(reporte, filas_reporte)
                archivo = exportar_reporte(datos, reporte.formato)
                _mostrar_descarga(
                    archivo,
                    etiqueta=f"Descargar {reporte.formato} · Reporte {reporte.id_reporte}",
                )
            except Exception as error:
                st.error(f"No se pudo preparar la descarga: {error}")


def mostrar_reportes(sistema):
    encabezado_pagina("Reportes academicos", periodo=sistema.periodo_actual)

    tab_generar, tab_resumen, tab_consulta = st.tabs(["Generar reporte", "Resumen", "Historial"])

    with tab_generar:
        intro_modulo(
            "Seleccione el contenido, periodo y formato. El documento se genera con los datos reales del sistema.",
            "📝",
        )
        panel_generar_reporte(
            sistema,
            obtener_rol_actual(),
            usuario=obtener_usuario_actual(sistema),
            prefijo="admin",
        )

    with tab_resumen:
        _resumen_reportes(sistema)

    with tab_consulta:
        _consulta_reportes(sistema)
