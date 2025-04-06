from collections import namedtuple
from engine.shell import ShellClient, CmdResult
from config import conf

VM_LABEL_LOCAL = "local"
VM_LABEL_VMC1 = "vmc1"


def _init_ssh_cli(shConf: dict):
    cli = ShellClient(name=shConf.get("name"), 
                      host=shConf.get("host"),
                      port=shConf.get("port"),
                      user=shConf.get("user"),
                      passwd=shConf.get("passwd"))
    return cli


env = "local"
local = _init_ssh_cli(conf.get_shell_conf(env, VM_LABEL_LOCAL))
vmc1 = _init_ssh_cli(conf.get_shell_conf(env, VM_LABEL_VMC1))


_label_to_ssh_cli = {
    VM_LABEL_LOCAL: local,
    VM_LABEL_VMC1: vmc1,
}


def get_ssh_cli(label: str):
    cli = _label_to_ssh_cli.get(label)
    return cli


def exists(label: str) -> bool:
    return label in _label_to_ssh_cli.keys()
