import streamlit as st
import pandas as pd
import numpy as np

from engine.shell import CmdResult
from view import vm_viewer
from vm import vm
from state.state import state


st.set_page_config(layout="wide")


with st.sidebar:
    st.markdown("# Vm page")

    clear = st.button("clear shell")
    if clear:
        state.clear_shells()


# ------------------------------------------------------------

t_vmc1, t_local, t_dev = st.tabs(["vmc1", "local", "dev"])


with t_local:
    vm_viewer.view_shells(label=vm.VM_LABEL_LOCAL)

with t_vmc1:
    vm_viewer.view_shells(label=vm.VM_LABEL_VMC1)
