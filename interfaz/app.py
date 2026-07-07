import sys
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from interfaz.state import get_sistema

st.set_page_config(page_title="Sistema de Nivelacion POO", layout="wide")

sistema = get_sistema()

st.sidebar.title("Menu")
st.sidebar.caption("Sistema de Nivelacion POO")

st.title("Sistema de Nivelacion POO")
st.info("Interfaz web en construccion.")
