
import json
import datetime
import inspect
from typing import NamedTuple, List, Dict, Any
from sqlalchemy import create_engine, Engine, Connection, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import ResultProxy 
import pandas as pd
from prettytable import PrettyTable
from collections import OrderedDict
import logging


logger = logging.getLogger(__name__)


class DBClient(object):
    def __init__(self, connection: str) -> None:
        self._conn_str = connection
        self._engine: Engine = create_engine(self._conn_str)

    @property
    def engine(self) -> Engine:
        return self._engine

    @property
    def session(self) -> Session:
        return sessionmaker(bind=self._engine)

    def connect(self) -> Connection:
        return self._engine.connect()

    def select(self, sql: str, params: dict = None) -> List[Dict[str, Any]]:
        """
        执行SQL查询并返回字典列表，select语句中不能有重复的字段
        :param sql: SQL查询语句
        :param params: 查询参数
        :return: 字典列表
        """
        logger.info(sql)

        with self.session() as sess:
            result: ResultProxy = sess.execute(text(sql), params or {})
            sess.commit()

        date_format: str = '%Y-%m-%d %H:%M:%S'
        # 处理结果并转换为字典列表
        dict_list = []
        for row in result:
            row_dict = OrderedDict()

            for idx, col in enumerate(result.keys()):
                value = row[idx]
                # 处理字段重复问题
                if col in row_dict:
                    logger.warning("duplicate column: {col}", col=col)
                    continue
                # 处理日期类型转换
                if isinstance(value, datetime.datetime):
                    value = value.strftime(date_format)
                row_dict[col] = value

            dict_list.append(row_dict)

        return dict_list


def get_fields(dict_list: List[Dict[str, Any]]) -> List[str]:
    # 获取处理后的字段名列表
    fields = list(dict_list[0].keys()) if dict_list else []
    return fields


def to_dataframe(dict_list: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    将字典列表转换为Pandas DataFrame
    """
    return pd.DataFrame(dict_list)


def print_pretty_table(
    dict_list: List[Dict[str, Any]],
    columns: List[str] = None,
    max_width: int = 80
):
    """
    使用PrettyTable打印美观的输出
    :param dict_list: 数据字典列表
    :param columns: 指定要显示的列（None表示全部）
    :param max_width: 列最大宽度（自动换行）
    """
    if not dict_list:
        logger.warning("No data to display")
        return

    table = PrettyTable()

    # 确定要显示的列
    display_columns = columns or list(dict_list[0].keys())
    table.field_names = display_columns

    # 设置列格式
    for field in table.field_names:
        table._max_width[field] = max_width
        table.align[field] = "l"

    for row in dict_list:
        table.add_row([row.get(col, '') for col in display_columns])

    print(table)


def _main():
    import utils

    utils.log_base_config()
    DATABASE_URL = "mysql+pymysql://test:test@dev.local:3306/test"
    db_cli = DBClient(connection=DATABASE_URL)
    res = db_cli.select("select * from users limit 3;")
    print_pretty_table(res)


if __name__ == "__main__":
    _main()
