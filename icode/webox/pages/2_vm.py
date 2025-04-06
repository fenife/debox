import streamlit as st
import pandas as pd
import numpy as np

from engine.shell import CmdResult
from view import vm_viewer
from vm import vm
from state import sess_state as ss


st.set_page_config(layout="wide")

ss.init_states()


with st.sidebar:
    st.markdown("# Vm page")

    clear = st.button("clear shell")
    if clear:
        ss.Shell.clear_all()


# ------------------------------------------------------------

t_vmc1, t_local, t_dev = st.tabs(["vmc1", "local", "dev"])


with t_local:
    vm_viewer.view_shells(label=vm.VM_LABEL_LOCAL)

with t_vmc1:
    vm_viewer.view_shells(label=vm.VM_LABEL_VMC1)
