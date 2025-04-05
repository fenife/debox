from typing import List, Union
import datetime
import fabric as fab
from invoke import Result, run
from streamlit import logger

class MultiCmdResult(object):
    def __init__(self, results: List["CmdResult"]):
        self.results = results

    def output(self):
        pass


class CmdResult(object):
    def __init__(self, dt: datetime.datetime, cli: "ShellClient",
                 cmd: str, resp: Result):
        self.dt: datetime.datetime = dt
        self.cmd: str = cmd
        self.resp: Result = resp
        self._cli: "ShellClient" = cli

    @property
    def origin(self):
        return self.resp

    @property
    def stdout(self):
        return self.resp.stdout

    @property
    def stderr(self):
        return self.resp.stderr

    @property
    def output(self):
        """
        # root @ vm (172.0.0.1) in /wine/devbox/icode [9:25:11] 
        $ <cmd>
        """
        c = self._cli
        dt_str = self.dt.strftime("%H:%M:%S")
        prefix = f"{c.user} @ {c.hostname} ({c.host}) in {c.pwd} [{dt_str}]"
        s = f"{prefix} \n$ {self.cmd}\n{self.stdout or self.stderr}"
        return s


class ShellClient(object):
    CMD_ECHO = "echo"
    CMD_PWD = "pwd"
    CMD_CD = "cd"

    def __init__(self, name=None, host=None, port=None, user=None, passwd=None):
        self.is_local = False
        if not host:
            host = "localhost"
            self.is_local = True
        self.host = host
        self.name = name or host
        self.port = port
        self.user = user
        self.passwd = passwd
        self._conn = None
        self._pwd = ""
        self._hostname = ""

    @property
    def conn(self) -> fab.Connection:
        if not self._conn:
            if self.is_local:
                self._conn = fab.Connection(host=self.host)
            else:
                self._conn = fab.Connection(
                    host=self.host, user=self.user,
                    connect_kwargs={"password": self.passwd})
        return self._conn

    # def runs(self, cmds: Union[str, List[str]], echo=True):
    #     if isinstance(cmds, str):
    #         cmds = [cmds]     # str -> [str]
    #     for cmd in cmds:
    #         if cmd == self.CMD_ECHO:
    #             self.echo()
    #         else:
    #             self.run(cmd, echo=echo)

    def _run(self, cmd, echo=True) -> Result:
        try:
            if self.is_local:
                resp = self.conn.local(cmd, echo=echo, warn=True)
            else:
                resp = self.conn.run(cmd, echo=echo, warn=True)
        except Exception as e:
            msg = str(e)
            resp = Result(command=cmd, stdout=msg, stderr=msg, exited=-1)

        return resp

    def run(self, cmd: str, echo=True) -> CmdResult:
        dt = datetime.datetime.now()
        resp = self._run(cmd, echo=echo)
        result = CmdResult(dt=dt, cli=self, cmd=cmd, resp=resp)
        return result

    def echo(self, echo=False):
        return self.run(self.CMD_ECHO, echo=echo)

    @property
    def pwd(self):
        if not self._pwd:
            r = self.run("pwd")
            self._pwd = r.stdout.strip()
        return self._pwd

    @property
    def hostname(self):
        if not self._hostname:
            r = self.run("hostname")
            self._hostname = r.stdout.strip()
        return self._hostname
