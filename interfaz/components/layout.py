import streamlit as st

from interfaz.components.cards import metric_card


def intro_modulo(descripcion, icono=""):
    prefijo = f"{icono} " if icono else ""
    st.markdown(f"{prefijo}{descripcion}")


def fila_metricas(metricas, columnas=4):
    cols = st.columns(columnas)
    for indice, (etiqueta, valor) in enumerate(metricas):
        with cols[indice % columnas]:
            metric_card(etiqueta, valor)


def tabla_o_vacio(filas, mensaje):
    if not filas:
        st.info(mensaje)
        return False
    st.dataframe(filas, use_container_width=True, hide_index=True)
    return True


def detalle_entidad(titulo, campos):
    with st.expander(titulo, expanded=False):
        for etiqueta, valor in campos:
            st.write(f"**{etiqueta}:** {valor}")


def tarjetas_navegacion(modulos, prefijo_clave="modulo", columnas=2):
    from interfaz.idioma import t
    from interfaz.navigation import navegar_a

    cols = st.columns(columnas)
    for indice, item in enumerate(modulos):
        if len(item) == 3:
            clave_interna, nombre, descripcion = item
        else:
            clave_interna = item[0]
            nombre = item[0]
            descripcion = item[1] if len(item) > 1 else ""

        with cols[indice % columnas]:
            with st.container(border=True):
                st.markdown(f"**{nombre}**")
                st.caption(descripcion)
                if st.button(
                    t("layout.ir_a", nombre=nombre),
                    key=f"{prefijo_clave}_{indice}_{clave_interna.replace(' ', '_')}",
                    use_container_width=True,
                ):
                    navegar_a(clave_interna)
