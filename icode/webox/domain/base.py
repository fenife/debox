
from engine.db import DBClient
from engine.http import HttpClient
from config import Config


class BaseDomainService(object):
    def __init__(self) -> None:
        self.db = DBClient(Config.db_conn_str())
        self.http = HttpClient(Config.yonder.host, Config.yonder.port)

