import streamlit as st

from servicios.exportador_reportes import (  # Importa funciones para generar y exportar reportes
    exportar_reporte,
    obtener_filas_reporte_por_rol,
    preparar_exportacion_directa,
    resumen_filas_reporte,
    tipos_reporte_por_rol,
)

# Crea una clave única para guardar datos en la sesión
def _clave_sesion(prefijo: str, nombre: str) -> str:
    return f"reporte_{prefijo}_{nombre}"

# Devuelve los cursos asignados al docente
def _cursos_docente(sistema, docente):
    return [curso for curso in sistema.cursos.values() if curso.docente == docente]

# Obtiene el nombre completo del usuario
def _nombre_usuario(usuario):
    if not usuario:
        return "Sistema"
    return f"{usuario.nombres} {usuario.apellidos}"

# Muestra el panel para generar reportes
def panel_generar_reporte(sistema, rol: str, usuario=None, prefijo: str = "general"):
    tipos = tipos_reporte_por_rol(rol) # Obtiene los tipos de reporte disponibles
    if not tipos:
        st.warning("No hay tipos de reporte disponibles para este rol.")
        return

    periodos = sistema.listar_periodos() or [sistema.periodo_actual or "Sin periodo"] # Lista los períodos académicos

    st.markdown("#### Configurar reporte")
    col_tipo, col_periodo = st.columns(2)
    with col_tipo:
        tipo_reporte = st.selectbox("Que desea incluir en el reporte?", tipos, key=_clave_sesion(prefijo, "tipo"))
    with col_periodo:
        periodo = st.selectbox("Periodo academico", periodos, key=_clave_sesion(prefijo, "periodo"))

    curso_id = None
    if rol == "Docente":
        cursos = _cursos_docente(sistema, usuario)
        if not cursos:
            st.info("No tiene cursos asignados para generar reportes.")
            return
        opciones_curso = {"Todos los cursos": "Todos"}
        opciones_curso.update({f"{curso.codigo} - {curso.nombre}": curso.id_curso for curso in cursos})
        etiqueta_curso = st.selectbox(
            "Filtrar por curso",
            list(opciones_curso.keys()),
            key=_clave_sesion(prefijo, "curso"),
        )
        curso_id = opciones_curso[etiqueta_curso]

    col_formato, col_desc = st.columns([1, 2]) # Selecciona formato y descripción
    with col_formato:
        formato = st.radio("Formato de descarga", ["PDF", "Excel"], horizontal=True, key=_clave_sesion(prefijo, "formato"))
    with col_desc:
        descripcion = st.text_input(
            "Titulo o descripcion del reporte",
            value=f"Reporte {tipo_reporte} - {periodo}",
            key=_clave_sesion(prefijo, "descripcion"),
        )

    filas = obtener_filas_reporte_por_rol( # Obtiene los datos del reporte
        sistema,
        rol,
        tipo_reporte,
        periodo,
        usuario=usuario,
        curso_id=curso_id,
    )
    st.caption(resumen_filas_reporte(filas)) # Muestra la cantidad de registros

    if filas: # Vista previa de los datos
        with st.expander("Vista previa de datos (primeros 15 registros)", expanded=False):
            st.dataframe(filas[:15], use_container_width=True, hide_index=True)
    else:
        st.warning("No hay datos con los filtros actuales. Ajuste el periodo o el tipo de reporte.")

    generar = st.button(  # Botón para generar el reporte
        "Generar documento",
        type="primary",
        use_container_width=True,
        key=_clave_sesion(prefijo, "generar"),
    )

    if generar:
        try:
            if not descripcion.strip():
                raise ValueError("Ingrese una descripcion para el reporte.")

            datos = preparar_exportacion_directa(
                tipo_reporte,
                periodo,
                descripcion.strip(),
                filas,
                generado_por=_nombre_usuario(usuario),
            )
            archivo = exportar_reporte(datos, formato)
            st.session_state[_clave_sesion(prefijo, "archivo")] = {
                "contenido": archivo.contenido,
                "nombre": archivo.nombre,
                "mime": archivo.mime,
                "formato": formato,
            }
            st.success(f"Documento {formato} generado correctamente ({len(filas)} registros).")
        except Exception as error:
            st.error(f"No se pudo generar el reporte: {error}")

    archivo_guardado = st.session_state.get(_clave_sesion(prefijo, "archivo"))
    if archivo_guardado:
        st.download_button( # Muestra el botón de descarga
            label=f"Descargar {archivo_guardado['formato']} · {archivo_guardado['nombre']}",
            data=archivo_guardado["contenido"],
            file_name=archivo_guardado["nombre"],
            mime=archivo_guardado["mime"],
            use_container_width=True,
            type="primary",
            key=_clave_sesion(prefijo, "descarga"),
        )
