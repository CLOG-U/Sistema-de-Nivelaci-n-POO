import streamlit as st
# Importa componentes de la interfaz
from interfaz.branding import encabezado_pagina
from interfaz.components.layout import detalle_entidad, fila_metricas, intro_modulo, tabla_o_vacio
from interfaz.components.tables import horario_to_dict

# Orden de los días de la semana
ORDEN_DIAS = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"]

# Formulario para registrar un horario
def _formulario_horario(sistema):
    if not sistema.aulas:
        st.warning("Debe registrar al menos un aula antes de crear un horario.")
        return

    opciones_aulas = {f"{aula.codigo} - {aula.nombre}": aula for aula in sistema.aulas.values()} # Lista de aulas disponibles

    with st.form("form_horario"): # Formulario de registro
        dia = st.selectbox("Dia", ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado"])
        hora_inicio = st.text_input("Hora inicio (HH:MM)")
        hora_fin = st.text_input("Hora fin (HH:MM)")
        modalidad = st.selectbox("Modalidad", ["Presencial", "Virtual", "Hibrida"])
        grupo = st.text_input("Grupo")
        aula_etiqueta = st.selectbox("Aula", list(opciones_aulas.keys()))
        enviado = st.form_submit_button("Registrar horario", use_container_width=True)

    if enviado: # Guarda el horario
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


def _resumen_horarios(sistema): # Muestra un resumen de los horarios
    intro_modulo("Planificacion de bloques horarios, modalidad y aulas asociadas.", "🕐")
    horarios = list(sistema.horarios.values())
    presencial = sum(1 for h in horarios if h.modalidad == "Presencial")
    virtual = sum(1 for h in horarios if h.modalidad == "Virtual")
    hibrida = sum(1 for h in horarios if h.modalidad == "Hibrida")

    fila_metricas( # Muestra métricas
        [
            ("Total horarios", len(horarios)),
            ("Presencial", presencial),
            ("Virtual", virtual),
            ("Hibrida", hibrida),
        ]
    )

    resumen_dia = sistema.resumen_horarios_por_dia()
    if resumen_dia:
        st.markdown("#### Distribucion por dia")
        st.bar_chart(resumen_dia)

# Consulta y filtra horarios
def _consulta_horarios(sistema):
    horarios = list(sistema.horarios.values())
    if not horarios:
        st.warning("No hay horarios registrados.")
        return

    filtro_dia = st.selectbox(
        "Filtrar por dia",
        ["Todos"]
        + sorted({h.dia for h in horarios}, key=lambda d: ORDEN_DIAS.index(d) if d in ORDEN_DIAS else 99),
    )
    if filtro_dia != "Todos":
        horarios = [h for h in horarios if h.dia == filtro_dia]

    filas = [horario_to_dict(horario) for horario in horarios]
    if not tabla_o_vacio(filas, "No hay horarios con ese filtro."):
        return

    for horario in horarios: # Muestra el detalle de cada horario
        aula = horario.aula
        detalle_entidad(
            f"{horario.dia} {horario.hora_inicio}-{horario.hora_fin} · Grupo {horario.grupo}",
            [
                ("Modalidad", horario.modalidad),
                ("Aula", f"{aula.codigo} - {aula.nombre}" if aula else "Sin aula"),
                ("Edificio", aula.edificio if aula else "N/A"),
            ],
        )

# Vista principal del módulo de horarios
def mostrar_horarios(sistema):
    encabezado_pagina("Gestion de horarios")

    tab_resumen, tab_registrar, tab_consulta = st.tabs(["Resumen", "Registrar", "Consulta"])

    with tab_resumen:
        _resumen_horarios(sistema)

    with tab_registrar:
        intro_modulo("Cree bloques horarios vinculados a un aula existente.", "📝")
        _formulario_horario(sistema)

    with tab_consulta:
        _consulta_horarios(sistema)
