import sys
from loguru import logger
import streamlit as st
from state import sess_state as ss

logger.remove()             # Remove default handler (and all others)
logger.add(sys.stdout, backtrace=False, diagnose=False)

st.set_page_config(layout="wide")

st.markdown("# main page")

ss.init_states()

