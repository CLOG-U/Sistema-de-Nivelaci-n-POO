import streamlit as st

from interfaz.branding import (
    COLOR_ROJO,
    COLOR_VERDE,
    FACULTAD,
    MODULO_POO,
    NOMBRE_SISTEMA,
    SIGLAS,
    UNIVERSIDAD,
    encabezado_pagina,
    mostrar_logo,
)


def mostrar_acerca(sistema):
    encabezado_pagina("Acerca del sistema", periodo=sistema.periodo_actual)

    ok_db, mensaje_db = sistema.probar_conexion_db()
    estado_db = "Conectada" if ok_db else "Modo demostracion"
    resumen = sistema.resumen()

    col_logo, col_info = st.columns([1, 2])
    with col_logo:
        mostrar_logo(ancho=200)
    with col_info:
        st.markdown(
            f"""
            ## {NOMBRE_SISTEMA}

            Plataforma institucional para la gestion integral de procesos de nivelacion academica
            en la **{FACULTAD}**, {UNIVERSIDAD} ({SIGLAS}).

            Desarrollada como solucion profesional bajo principios de Programacion Orientada a Objetos,
            con arquitectura modular, persistencia en base de datos y control de acceso por roles.
            """
        )

    st.markdown(
        f"""
        <div style="display:flex;gap:12px;flex-wrap:wrap;margin:12px 0 20px 0;">
            <span style="background:{COLOR_VERDE};color:white;padding:6px 14px;border-radius:20px;font-size:0.85rem;">
                Version academica 2026
            </span>
            <span style="background:{COLOR_ROJO};color:white;padding:6px 14px;border-radius:20px;font-size:0.85rem;">
                Periodo activo: {sistema.periodo_actual}
            </span>
            <span style="background:#2D2D2D;color:white;padding:6px 14px;border-radius:20px;font-size:0.85rem;">
                {MODULO_POO}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_general, tab_tecnico, tab_roles, tab_soporte = st.tabs(
        ["Vision general", "Arquitectura", "Roles y permisos", "Soporte"]
    )

    with tab_general:
        st.markdown("### Proposito del sistema")
        st.markdown(
            f"""
            {NOMBRE_SISTEMA} centraliza la operacion academica de nivelacion: registro de usuarios,
            planificacion de aulas y horarios, gestion de cursos, matriculas, cargas academicas,
            seguimiento de calificaciones y asistencia, e importacion masiva de datos institucionales.

            La plataforma esta disenada para uso administrativo, docente y estudiantil, con una
            experiencia web accesible desde navegador y despliegue en la nube.
            """
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Usuarios", resumen.get("usuarios", 0))
        c2.metric("Cursos", resumen.get("cursos", 0))
        c3.metric("Matriculas", resumen.get("matriculas", 0))
        c4.metric("Reportes", resumen.get("reportes", 0))

        st.markdown("### Capacidades principales")
        st.markdown(
            """
            - **Gestion academica:** usuarios, aulas, horarios, cursos e inscripciones por periodo.
            - **Seguimiento:** calificaciones (escala 0-10, aprobado >= 7.0) y control de asistencia.
            - **Reportes exportables:** documentos PDF y Excel filtrables por rol y periodo.
            - **Importacion CSV:** carga masiva unificada con columna `tipo_registro`.
            - **Internacionalizacion:** interfaz en espanol e ingles (menus y dashboards).
            - **Identidad ULEAM:** branding institucional con logos oficiales.
            """
        )

    with tab_tecnico:
        st.markdown("### Stack tecnologico")
        st.markdown(
            """
            | Componente | Tecnologia |
            |------------|------------|
            | Backend | Python 3 · Programacion Orientada a Objetos |
            | Interfaz | Streamlit (aplicacion web reactiva) |
            | Base de datos | Microsoft SQL Server (`PROYECTOPOO`) |
            | Reportes | `fpdf2` (PDF) · `openpyxl` (Excel) |
            | Conectividad | `pyodbc` · ODBC Driver 17 |
            | Despliegue | Streamlit Cloud |
            """
        )

        st.markdown("### Patrones de diseno aplicados")
        st.markdown(
            """
            - **Herencia y polimorfismo:** jerarquia de usuarios (Administrador, Docente, Estudiante).
            - **Factory Method:** creacion tipada de entidades del dominio academico.
            - **Facade:** proceso de matricula e inscripcion simplificado (`MatriculaFacade`).
            - **Strategy:** exportacion de reportes en distintos formatos (`IExportable`).
            - **Singleton:** gestor de idioma y configuracion de sesion.
            - **Repository:** capa de persistencia SQL con fallback en memoria.
            """
        )

        st.markdown("### Estado de persistencia")
        if ok_db:
            st.success(f"Base de datos SQL Server operativa. {mensaje_db}")
        else:
            st.warning(
                f"{mensaje_db} El sistema funciona en modo demostracion en memoria. "
                "Configure `[database]` en Streamlit Secrets para conexion a SQL Server."
            )

    with tab_roles:
        st.markdown("### Modelo de acceso")
        st.markdown(
            """
            El acceso se realiza con **cedula o correo institucional** (`@uleam.edu.ec`) y contrasena.
            El rol se determina automaticamente segun el tipo de usuario registrado; no puede elegirse manualmente.
            """
        )

        st.markdown("#### Administrador")
        st.markdown(
            "Gestion completa: usuarios, infraestructura (aulas/horarios), cursos, inscripciones, "
            "cargas academicas, importacion de datos, reportes institucionales y supervision del sistema."
        )

        st.markdown("#### Docente")
        st.markdown(
            "Consulta de cursos asignados, horarios, listado de estudiantes, registro de notas y asistencia, "
            "y generacion de reportes academicos limitados a sus cursos."
        )

        st.markdown("#### Estudiante")
        st.markdown(
            "Consulta de cursos inscritos, horario personal, carga academica, perfil con calificaciones "
            "y asistencia, y descarga de reportes personales del periodo."
        )

    with tab_soporte:
        st.markdown("### Informacion de despliegue")
        st.markdown(
            """
            - **Entorno de produccion:** [sistema-nivelacion-poo.streamlit.app](https://sistema-nivelacion-poo.streamlit.app)
            - **Ejecucion local:** `streamlit run interfaz/app.py`
            - **Script de base de datos:** `POOPROYECTO.sql`
            - **Repositorio:** [GitHub — Sistema-de-Nivelacion-POO](https://github.com/CLOG-U/Sistema-de-Nivelacion-POO)
            """
        )

        st.markdown("### Escala academica")
        st.info(
            "Las calificaciones se registran en escala **0 a 10**. "
            "El estudiante aprueba con promedio final **mayor o igual a 7.0**."
        )

        st.markdown("### Contacto institucional")
        st.markdown(
            f"""
            Para soporte academico o administrativo, contacte a la {FACULTAD}
            de la {UNIVERSIDAD}.

            **Estado actual del servicio:** {estado_db} · Periodo {sistema.periodo_actual}
            """
        )
