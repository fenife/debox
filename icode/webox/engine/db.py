
import datetime
import inspect
from typing import NamedTuple, List
from loguru import logger
import streamlit as st
from streamlit.connections import SQLConnection
from pandas import DataFrame
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker


class DBResult(object):
    def __init__(self, dt: datetime.datetime, sql: str,
                 df: DataFrame, label: str = "") -> None:
        self.dt = dt        # query timestamp
        self.sql = sql
        self.df = df
        self.label = label
        self.desc = ""
        self.caller = inspect.stack()[2].function


    def items(self, name: str = "", is_reversed: bool = False) -> List[NamedTuple]:
        """
        return namedtuple list from dataframe
        """
        if not name:
            name = self.label
        df = self.df
        if is_reversed:
            df = self.df[::-1].reset_index(drop=True)
        d = list(df.itertuples(name=name))
        return d


class DBClient(object):
    def __init__(self, db_conn_str: str) -> None:
        self._conn_str = db_conn_str
        self._engine: Engine = create_engine(self._conn_str)
        self._st_conn = None

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def session(self):
        return sessionmaker(bind=self._engine)

    def _query(self, sql: str):
        print(sql)
        with self.session() as s:
            print(s.query(sql).all())

    def query(self, sql: str, label="", *args, **kwargs) -> DBResult:
        logger.info(sql)
        now = datetime.datetime.now()
        df = self.st_conn.query(sql, ttl=1, *args, **kwargs)
        result = DBResult(dt=now, sql=sql, df=df, label=label)
        return result

    @property
    def st_conn(self) -> SQLConnection:
        if not self._st_conn:
            self._st_conn = st.connection(
                "local_db",
                type="sql",
                url=self._conn_str,
            )
        return self._st_conn

    def st_query(self, sql: str, label="", *args, **kwargs) -> DataFrame:
        result = self.query(sql, label=label, *args, **kwargs)
        return result.df
