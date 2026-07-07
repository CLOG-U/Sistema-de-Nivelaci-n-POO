import streamlit as st


def aplicar_estilos():
    st.markdown(
        """
        <style>
            .main {
                background-color: #f4f6f8;
            }
            [data-testid="stSidebar"] {
                background-color: #1e3a5f;
            }
            [data-testid="stSidebar"] * {
                color: #ffffff !important;
            }
            [data-testid="stMetric"] {
                background-color: #ffffff;
                border: 1px solid #dbe2ea;
                border-radius: 10px;
                padding: 12px;
            }
            [data-testid="stForm"] {
                background-color: #ffffff;
                border: 1px solid #dbe2ea;
                border-radius: 10px;
                padding: 16px;
            }
            h1, h2, h3 {
                color: #1e3a5f;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
