import sys
from loguru import logger
import streamlit as st
from state import sess_state as ss
from config import conf
import json

logger.remove()             # Remove default handler (and all others)
logger.add(sys.stdout, backtrace=False, diagnose=False)

st.set_page_config(layout="wide")

st.markdown("# main page")

ss.init_states()


env = st.selectbox(label="env", index=None,
                   options=["local", "dev", None])
if env:
    ss.Env.set_env(env)

env_configs = conf.get_env_configs(ss.Env.get_env())
st.code(json.dumps(env_configs, indent=2), wrap_lines=True)
