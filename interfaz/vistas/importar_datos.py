import streamlit as st
# Importa funciones y componentes necesarios
from interfaz.auth import obtener_usuario_actual
from interfaz.branding import encabezado_pagina
from interfaz.components.layout import intro_modulo, tabla_o_vacio
from interfaz.idioma import t
from modelos.admin import Administrador
from servicios.importador_csv import (
    ORDEN_TIPOS_REGISTRO,
    contar_por_tipo,
    importar_dataset,
    leer_csv,
    obtener_plantilla_csv,
    validar_modelo_dataset,
)

# Devuelve la etiqueta traducida del tipo de registro
def _etiqueta_tipo(tipo: str) -> str:
    return t(f"import.tipo.{tipo}")

# Genera el resumen de la estructura del archivo CSV
def _resumen_modelo():
    filas = []
    for indice, tipo in enumerate(ORDEN_TIPOS_REGISTRO, start=1):
        filas.append(
            {
                "Orden": indice,
                "tipo_registro": tipo,
                "Descripcion": t(f"import.desc.{tipo}"),
            }
        )
    return filas

# Muestra el resultado de la importación
def _mostrar_resultado(resultado):
    if resultado.hubo_exito:
        st.success(
            t(
                "import.resultado_dataset_ok",
                importadas=resultado.importadas,
                total=resultado.total_filas,
            )
        )
    elif resultado.importadas:
        st.warning(
            t(
                "import.resultado_dataset_parcial",
                importadas=resultado.importadas,
                total=resultado.total_filas,
            )
        )
    else:
        st.error(t("import.resultado_vacio"))
# Muestra registros omitidos
    if resultado.omitidas:
        st.warning(t("import.resultado_omitidas", omitidas=resultado.omitidas))

    if resultado.resumen_por_tipo: # Muestra el resumen por tipo de registro
        st.markdown(f"**{t('import.resumen_fases')}**")
        resumen_filas = [
            {
                "Fase": _etiqueta_tipo(tipo),
                "Total": datos["total"],
                "Importadas": datos["importadas"],
                "Omitidas": datos["omitidas"],
            }
            for tipo, datos in resultado.resumen_por_tipo.items()
        ]
        st.dataframe(resumen_filas, use_container_width=True, hide_index=True)

    if resultado.errores: # Muestra errores encontrados
        st.markdown(f"**{t('import.errores_titulo')}**")
        for error in resultado.errores[:50]:
            st.markdown(f"- {error}")
        if len(resultado.errores) > 50:
            st.caption(t("import.errores_mas", extra=len(resultado.errores) - 50))

# Muestra la guía de importación
def _tab_guia():
    intro_modulo(t("import.intro_guia_unificado"), "📋")
    st.markdown(t("import.orden_recomendado_unificado"))
    tabla_o_vacio(_resumen_modelo(), t("import.sin_tipos"))

    st.divider()
    st.markdown(f"**{t('import.notas_titulo')}**")      # Muestra recomendaciones
    st.markdown(t("import.nota_persistencia"))
    st.markdown(t("import.nota_referencias"))
    st.markdown(t("import.nota_duplicados"))


def _tab_importar(sistema):
    intro_modulo(t("import.intro_importar_unificado"), "📥")

    st.download_button(
        t("import.descargar_plantilla"),
        data=obtener_plantilla_csv(),
        file_name="plantilla_dataset_nivelacion.csv",
        mime="text/csv",
        use_container_width=True,
    )

    archivo = st.file_uploader(t("import.subir_csv_unificado"), type=["csv"], key="csv_dataset")

    if not archivo:
        return

    filas = leer_csv(archivo.getvalue())
    if not filas:
        st.warning(t("import.archivo_vacio"))
        return

    errores = validar_modelo_dataset(filas)
    if errores:
        for error in errores[:20]:
            st.error(error)
        return

    conteo = contar_por_tipo(filas)
    st.markdown(f"**{t('import.conteo_tipos')}**")
    st.dataframe(
        [{"tipo_registro": k, "filas": v} for k, v in sorted(conteo.items())],
        use_container_width=True,
        hide_index=True,
    )

    preview = [{k: v for k, v in fila.items() if k != "_fila_csv"} for fila in filas[:5]]  # Muestra una vista previa
    st.markdown(f"**{t('import.vista_previa')}** ({min(len(filas), 5)} / {len(filas)})")
    st.dataframe(preview, use_container_width=True, hide_index=True)

    if st.button(t("import.ejecutar_dataset"), type="primary", use_container_width=True): # Ejecuta la importación
        with st.spinner(t("import.importando")):
            resultado = importar_dataset(sistema, filas)
        _mostrar_resultado(resultado)

# Vista principal del módulo de importación
def mostrar_importar_datos(sistema):
    encabezado_pagina(t("import.titulo"), periodo=sistema.periodo_actual)

    administrador = obtener_usuario_actual(sistema)
    if not isinstance(administrador, Administrador):
        st.error(t("import.solo_admin"))
        return

    if not st.session_state.get("db_cargada"):
        st.info(t("import.modo_demo"))

    tab_guia, tab_importar = st.tabs([t("import.tab_guia"), t("import.tab_importar")])

    with tab_guia:
        _tab_guia()

    with tab_importar:
        _tab_importar(sistema)
