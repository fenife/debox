
from engine.db import DBClient
from engine.http import HttpClient
from config import conf
from state import sess_state as ss


def get_db_conn_str(dbConf: dict):
    # mysql+pymysql://user:passkey@localhost:port/db?charset=utf8mb4
    s = "mysql+pymysql://{u}:{p}@{h}:{port}/{db}?charset={c}".format(
        u=dbConf.get("user"), p=dbConf.get("passwd"),
        h=dbConf.get("host"), port=dbConf.get("port"),
        db=dbConf.get("database"), c=dbConf.get("charset"),
    )
    return s


class BaseDomainService(object):
    def __init__(self) -> None:
        self._db_clients = {}
        self._http_clients = {}

    @property
    def db(self):
        env = ss.Env.get_env()
        dbCli = self._db_clients.get(env, None)
        if dbCli:
            return dbCli

        dbConf = conf.get_db_conf(env)
        dbCli = DBClient(get_db_conn_str(dbConf))
        self._db_clients[env] = dbCli
        return dbCli

    @property
    def http(self):
        env = ss.Env.get_env()
        httpCli = self._http_clients.get(env, None)
        if httpCli:
            return httpCli

        serverConf = conf.get_server_conf(env)
        host = serverConf.get("host")
        port = serverConf.get("port")
        httpCli = HttpClient(host=host, port=port)
        self._http_clients[env] = httpCli
        return httpCli

