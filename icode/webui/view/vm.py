import streamlit as st
import pandas as pd
import numpy as np

from engine.shell import CmdResult
import view
from vm import vm
from state.state import state


# ------------------------------------------------------------

_label_to_state_shell_key = {
    vm.VM_LABEL_LOCAL: state.local_shells,
    vm.VM_LABEL_VMC1: state.vmc1_shells,
}


class VmShellViewer(object):

    @staticmethod
    def _get_state_key(label: str):
        return _label_to_state_shell_key.get(label)

    def view_button_cmd(self, label: str):
        sk = self._get_state_key(label=label)
        btn_cmd = ""
        with st.container(border=True):
            spec = [0.5, 0.6, 0.5, 1, 1, 2, 1, 1, 1]
            c_ls, c_pwd, c_ip, c_ipt, c_ipset, c_grep, _, _, c_clear = \
                st.columns(spec, gap="small")

            if c_ls.button("ls", key=f"cmd:button:ls:{label}"):
                btn_cmd = "ls"
            if c_pwd.button("pwd", key=f"cmd:button:pwd:{label}"):
                btn_cmd = "pwd"
            if c_ip.button("ip", key=f"cmd:button:ip:{label}"):
                btn_cmd = "ip addr"
            if c_ipt.button("iptables", key=f"cmd:button:iptables:{label}"):
                btn_cmd = "iptables -nvL"
            if c_ipset.button("ipset", key=f"cmd:button:ipset:{label}"):
                btn_cmd = "ipset list"
            grep = c_grep.text_input("grep", key=f"cmd:button:grep:{label}",
                                     placeholder="grep",
                                     label_visibility="collapsed")
            if c_clear.button("clear", key=f"cmd:button:clear:{label}"):
                state.set(sk, [])

            if btn_cmd and grep:
                btn_cmd += f" | grep -v grep | grep {grep}"
        return btn_cmd

    def view_input_cmd(self, label: str):
        input_cmd = ""
        with st.container(border=True):
            input_cmd = st.chat_input("command", key=f"cmd:input:{label}")
        return input_cmd

    def view_shells(self, label: str):
        if not vm.exists(label=label):
            st.warning("no ssh cli label")
            return

        cli = vm.get_ssh_cli(label=label)
        sk = self._get_state_key(label=label)

        btn_cmd = self.view_button_cmd(label=label)
        input_cmd = self.view_input_cmd(label=label)
        cmd = btn_cmd or input_cmd
        if cmd:
            r = cli.run(cmd)
            st.session_state[sk].append(r)

        self._show_shells(label=label)

    def _show_shells(self, label: str):
        sk = self._get_state_key(label=label)
        with st.container(border=True):
            for r in reversed(st.session_state[sk]):
                st.code(r.output)
