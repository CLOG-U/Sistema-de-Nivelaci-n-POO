import streamlit as st

from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.layout import intro_modulo, tabla_o_vacio
from interfaz.components.tables import asistencia_registro_to_dict, calificacion_registro_to_dict, usuario_to_dict


def _cursos_docente(sistema, docente):
    return [curso for curso in sistema.cursos.values() if curso.docente == docente]


def _consulta_estudiantes(sistema, docente, curso):
    if not curso.lista_estudiantes:
        st.info("Este curso no tiene estudiantes inscritos.")
        return

    filas = []
    for estudiante in curso.lista_estudiantes:
        fila = usuario_to_dict(estudiante)
        fila["Estado nivelacion"] = estudiante.estado_nivelacion
        filas.append(fila)

    st.dataframe(filas, use_container_width=True, hide_index=True)


def _formulario_notas(sistema, docente, curso):
    if not curso.lista_estudiantes:
        st.warning("No hay estudiantes inscritos en este curso.")
        return

    opciones = {
        f"{e.nombres} {e.apellidos} · {e.cedula}": e for e in curso.lista_estudiantes
    }

    with st.form(f"form_notas_{curso.id_curso}"):
        estudiante_etiqueta = st.selectbox("Estudiante", list(opciones.keys()))
        parcial1 = st.number_input("Parcial 1", min_value=0.0, max_value=10.0, step=0.1, value=7.0)
        parcial2 = st.number_input("Parcial 2", min_value=0.0, max_value=10.0, step=0.1, value=7.0)
        observacion = st.text_input("Observacion")
        enviado = st.form_submit_button("Registrar notas", use_container_width=True)

    if enviado:
        try:
            estudiante = opciones[estudiante_etiqueta]
            calificacion = sistema.registrar_calificacion(
                docente,
                curso,
                estudiante,
                parcial1,
                parcial2,
                observacion=observacion.strip(),
            )
            st.success(
                f"Notas registradas para {estudiante.nombres}. "
                f"Nota final: {calificacion.nota_final} · Estado: {calificacion.estado}"
            )
        except Exception as error:
            st.error(str(error))


def _formulario_asistencia(sistema, docente, curso):
    if not curso.lista_estudiantes:
        st.warning("No hay estudiantes inscritos en este curso.")
        return

    opciones = {
        f"{e.nombres} {e.apellidos} · {e.cedula}": e for e in curso.lista_estudiantes
    }

    with st.form(f"form_asistencia_{curso.id_curso}"):
        estudiante_etiqueta = st.selectbox("Estudiante", list(opciones.keys()), key=f"asist_est_{curso.id_curso}")
        fecha = st.text_input("Fecha (AAAA-MM-DD)", value="2026-03-15")
        estado = st.selectbox("Estado", ["Presente", "Ausente", "Justificado", "Tardanza"])
        observacion = st.text_input("Observacion")
        enviado = st.form_submit_button("Registrar asistencia", use_container_width=True)

    if enviado:
        try:
            estudiante = opciones[estudiante_etiqueta]
            asistencia = sistema.registrar_asistencia(
                docente,
                curso,
                estudiante,
                fecha.strip(),
                estado,
                observacion=observacion.strip(),
            )
            st.success(
                f"Asistencia registrada para {estudiante.nombres} "
                f"el {asistencia.fecha}: {asistencia.estado}"
            )
        except Exception as error:
            st.error(str(error))


def mostrar_estudiantes_docente(sistema):
    encabezado_pagina("Mis estudiantes", periodo=sistema.periodo_actual)

    docente = obtener_usuario_actual(sistema)
    if not docente:
        st.warning("No hay docente seleccionado.")
        return

    cursos_docente = _cursos_docente(sistema, docente)
    if not cursos_docente:
        st.info("Este docente no tiene cursos asignados.")
        return

    opciones = {f"{curso.codigo} - {curso.nombre}": curso for curso in cursos_docente}
    curso_etiqueta = st.selectbox("Seleccione un curso", list(opciones.keys()))
    curso = opciones[curso_etiqueta]

    tab_consulta, tab_notas, tab_asistencia = st.tabs(["Consulta", "Registrar notas", "Registrar asistencia"])

    with tab_consulta:
        intro_modulo("Estudiantes inscritos en el curso seleccionado.", "📋")
        _consulta_estudiantes(sistema, docente, curso)

        calificaciones = [
            calificacion_registro_to_dict(registro)
            for registro in sistema.calificaciones.values()
            if registro["curso"] == curso
        ]
        asistencias = [
            asistencia_registro_to_dict(registro)
            for registro in sistema.asistencias.values()
            if registro["curso"] == curso
        ]
        st.markdown("#### Calificaciones del curso")
        tabla_o_vacio(calificaciones, "Sin calificaciones.")
        st.markdown("#### Asistencias del curso")
        tabla_o_vacio(asistencias, "Sin asistencias.")

    with tab_notas:
        intro_modulo("Registre notas usando Docente.registrar_notas() y el modelo Calificacion.", "📝")
        _formulario_notas(sistema, docente, curso)

    with tab_asistencia:
        intro_modulo("Registre asistencia usando Docente.registrar_asistencia() y el modelo Asistencia.", "📝")
        _formulario_asistencia(sistema, docente, curso)
