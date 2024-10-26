import sys
from loguru import logger
import streamlit as st
from state.state import state

logger.remove()             # Remove default handler (and all others)
logger.add(sys.stdout, backtrace=False, diagnose=False)

st.set_page_config(layout="wide")

st.markdown("# main page")

state.init_all()
