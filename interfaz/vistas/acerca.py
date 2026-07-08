import streamlit as st

from interfaz.branding import (
    FACULTAD,
    MODULO_POO,
    NOMBRE_SISTEMA,
    SIGLAS,
    UNIVERSIDAD,
    encabezado_pagina,
)


def mostrar_acerca(sistema):
    encabezado_pagina("Acerca del sistema", periodo=sistema.periodo_actual)

    ok_db, mensaje_db = sistema.probar_conexion_db()
    estado_db = "Conectada" if ok_db else "No disponible (modo en memoria)"

    st.markdown(
        f"""
        ### {SIGLAS} · {UNIVERSIDAD}

        **{NOMBRE_SISTEMA}** es una aplicacion web desarrollada para la gestion
        academica de procesos de nivelacion en la {FACULTAD}.

        - **Asignatura:** {MODULO_POO}
        - **Periodo academico activo:** {sistema.periodo_actual}
        - **Tecnologia:** Python, POO y Streamlit
        - **Correos institucionales:** dominio `@uleam.edu.ec`

        ### Funcionalidades

        - Gestion de usuarios, aulas, horarios y cursos
        - Inscripciones con MatriculaFacade y periodos academicos
        - Cargas academicas, calificaciones y asistencia
        - Generacion de reportes en PDF y Excel

        ### Patrones POO aplicados

        Herencia, polimorfismo, Factory Method, Facade y Strategy.

        ### Acceso por roles

        El sistema utiliza una interfaz diferenciada por roles, permitiendo que
        administradores, docentes y estudiantes accedan unicamente a las funciones
        correspondientes a su perfil.
        """
    )

    st.info(f"Institucion: {UNIVERSIDAD} ({SIGLAS})")

    st.markdown("### Estado de persistencia (BD-01 / BD-02 / BD-03)")
    if ok_db:
        st.success(mensaje_db)
    else:
        st.warning(
            f"{mensaje_db} Configure `[database]` en Streamlit Secrets para SQL Server. "
            "En Streamlit Cloud use `packages.txt` con unixODBC (BD-03)."
        )
