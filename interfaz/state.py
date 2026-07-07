import sys
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from servicios.sistema_nivelacion import SistemaNivelacion


def get_sistema():
    if "sistema" not in st.session_state:
        st.session_state.sistema = SistemaNivelacion()
        st.session_state.sistema.cargar_datos_demo()
    return st.session_state.sistema
