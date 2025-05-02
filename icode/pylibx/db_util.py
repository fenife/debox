
import json
import datetime
import inspect
import logging
import pandas as pd
from prettytable import PrettyTable
from collections import OrderedDict
from typing import NamedTuple, List, Dict, Any, Union
import sqlalchemy as sa
from sqlalchemy import create_engine, Engine, Connection, text
from sqlalchemy.orm import sessionmaker, Session, Query
from sqlalchemy.engine import ResultProxy
from sqlalchemy import or_, and_, not_, ColumnElement


logger = logging.getLogger(__name__)

_negated_op = {
    "eq": "ne",
    "ne": "eq",
    "gt": "le",
    "lt": "ge",
    "ge": "lt",
    "le": "gt",
    "like": "notlike",
    "in": "notin"
}


def dict_to_sa_filter(
    model: Any,
    filter_dict: Dict[str, Any]
) -> Union[ColumnElement[bool], None]:
    """
    增强版字典转查询条件解析器
    新增支持操作符：
    - not: 逻辑非
    - isnull: 空值判断
    - 自动处理布尔表达式
    """
    clauses = []

    for key, value in filter_dict.items():
        key_lower = key.lower()

        # 处理逻辑运算符
        if key_lower == "or":
            if not isinstance(value, list):
                raise ValueError("OR 条件需要数组格式")
            return or_(*[dict_to_sa_filter(model, sub) for sub in value])

        elif key_lower == "and":
            if not isinstance(value, list):
                raise ValueError("AND 条件需要数组格式")
            return and_(*[dict_to_sa_filter(model, sub) for sub in value])

        elif key_lower == "not":
            if not isinstance(value, dict):
                raise ValueError("NOT 条件需要字典格式")
            return not_(dict_to_sa_filter(model, value))

        # 处理字段条件
        else:
            if "__" in key:
                field_name, operator = key.split("__", 1)
            else:
                field_name, operator = key, "eq"

            column = getattr(model, field_name, None)
            if not column:
                raise AttributeError(f"模型 {model} 没有字段 {field_name}")

            # 扩展操作符映射
            if operator == "eq":
                clauses.append(column == value)
            elif operator == "ne":
                clauses.append(column != value)
            elif operator == "gt":
                clauses.append(column > value)
            elif operator == "lt":
                clauses.append(column < value)
            elif operator == "ge":
                clauses.append(column >= value)
            elif operator == "le":
                clauses.append(column <= value)
            elif operator == "like":
                clauses.append(column.like(value))
            elif operator == "in":
                clauses.append(column.in_(value))
            elif operator == "isnull":
                # 处理 IS NULL / IS NOT NULL
                if value is True:
                    clauses.append(column.is_(None))
                elif value is False:
                    clauses.append(column.isnot(None))
                else:
                    raise ValueError("isnull 只接受布尔值 True/False")
            elif operator == "not":
                # 处理字段级 NOT 操作
                if isinstance(value, dict) and len(value) == 1:
                    sub_op, sub_val = next(iter(value.items()))
                    negated_op = _negated_op.get(sub_op, sub_op)
                    cond = dict_to_sa_filter(
                        model,
                        {f"{field_name}__{negated_op}": sub_val}
                    )
                    clauses.append(cond)
                else:
                    raise ValueError("NOT 操作符需要单个条件字典")
            else:
                raise ValueError(f"不支持的运算符: {operator}")

    return and_(*clauses) if clauses else None


def build_query(
    session: Session,
    model: Any = None,
    query: Query = None,
    filters: Dict[str, Any] = None,
    limit: int = None,
) -> Query:
    """
    构建带过滤条件的查询
    """
    if not any([model, query]):
        raise Exception("model or query should not be empty")
    query = query or session.query(model)
    condition = dict_to_sa_filter(model, filters)
    if condition is not None:
        query = query.filter(condition)
    if limit is not None:
        query = query.limit(limit=limit)
    return query


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

        logger.info("row count: %s", len(dict_list))
        return dict_list

    def query(
            self,
            model: Any = None,
            query: Query = None,
            filters: Dict[str, Any] = None,
            limit: int = None,
    ) -> List[Any]:
        result = None
        try:
            with self.session() as sess:
                q = build_query(sess, model=model, query=query,
                                filters=filters, limit=limit)
                # logger.info("query: %s" % str(q))
                result = q.all()
        except Exception as e:
            logger.exception("query failed: %s", e)

        result_len = len(result) if result else 0
        logger.info("row count: %s", result_len)
        return result


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
