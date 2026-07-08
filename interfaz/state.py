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
        ok, mensaje = st.session_state.sistema.cargar_desde_db()
        st.session_state.db_cargada = ok
        st.session_state.db_mensaje = mensaje
        if not ok:
            st.session_state.sistema = None
    return st.session_state.sistema
