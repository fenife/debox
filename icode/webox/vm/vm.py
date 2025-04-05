from collections import namedtuple

from engine.shell import ShellClient, CmdResult
from config import Config

VM_LABEL_LOCAL = "local"
VM_LABEL_VMC1 = "vmc1"


def _init_ssh_cli(c):
    cli = ShellClient(name=c.name, host=c.host, port=c.port,
                      user=c.user, passwd=c.passwd)
    return cli


local = _init_ssh_cli(Config.local)
vmc1 = _init_ssh_cli(Config.vmc1)


_label_to_ssh_cli = {
    VM_LABEL_LOCAL: local,
    VM_LABEL_VMC1: vmc1,
}

def get_ssh_cli(label: str):
    cli = _label_to_ssh_cli.get(label)
    return cli

def exists(label: str) -> bool:
    return label in _label_to_ssh_cli.keys()
