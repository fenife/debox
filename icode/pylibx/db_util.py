
import json
import datetime
import inspect
import logging
import pandas as pd
from prettytable import PrettyTable
from collections import OrderedDict
from typing import NamedTuple, List, Dict, Any, Union, Type, TypeVar, \
    Optional, Set, Callable
import sqlalchemy as sa
from sqlalchemy import create_engine, Engine, Connection, text
from sqlalchemy.orm import sessionmaker, Session, Query, class_mapper, \
    relationship, declarative_base, Mapper, RelationshipProperty
from sqlalchemy.orm.properties import ColumnProperty
from sqlalchemy.engine import ResultProxy
from sqlalchemy import or_, and_, not_, ColumnElement


logger = logging.getLogger(__name__)

Base = declarative_base()

DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


_g_format_types = {
    datetime.date: lambda x: x.strftime(DATE_FORMAT) if x else None,
    datetime.datetime: lambda x: x.strftime(DATETIME_FORMAT) if x else None,
}

_g_type_converters = {
    sa.String: lambda x: x.strip() if isinstance(x, str) else x,
    sa.DATE: lambda x: datetime.datetime.strptime(x, DATE_FORMAT)
    if isinstance(x, str) else x,
    sa.DateTime: lambda x: datetime.datetime.strptime(x, DATETIME_FORMAT)
    if isinstance(x, str) else x,
}


class ModelMixin(object):

    def to_dict(
        self,
        exclude: Set[str] = None,
        format_types: Dict[Type, Callable[[Any], Any]] = None,
        visited: Set[int] = None
    ) -> Dict[str, Any]:
        """
        将 ORM 模型实例转换为字典

        Args:
            exclude: 要排除的属性名集合
            format_types: 类型格式化函数字典,
            visited: 防止循环引用的已访问对象集合（内部使用）

        Returns:
            转换后的字典
        """
        if exclude is None:
            exclude = set()

        if format_types is None:
            format_types = _g_format_types

        # 防止循环引用
        if visited is None:
            visited = set()

        instance_id = id(self)
        if instance_id in visited:
            return None
        visited.add(instance_id)

        # mapper: Mapper = inspect(self.__class__)
        mapper = class_mapper(self.__class__)
        result = {}

        # 处理普通列
        for column in mapper.columns:
            if column.key in exclude:
                continue
            value = getattr(self, column.key)
            # # 应用类型格式化
            formatter = format_types.get(type(value))
            if formatter:
                value = formatter(value)
            # for type_, formatter in format_types.items():
            #     if isinstance(value, type_):
            #         value = formatter(value)
            #         break
            result[column.key] = value

        # 处理关系属性
        for rel in mapper.relationships:
            if rel.key in exclude:
                continue

            related_obj = getattr(self, rel.key)

            if related_obj is None:
                result[rel.key] = None
            elif isinstance(rel, RelationshipProperty):
                if rel.uselist:  # 一对多或多对多关系
                    result[rel.key] = [
                        child.to_dict(
                            exclude=exclude,
                            format_types=format_types,
                            visited=visited.copy()
                        )
                        for child in related_obj
                    ]
                else:  # 多对一或一对一关系
                    result[rel.key] = related_obj.to_dict(
                        exclude=exclude,
                        format_types=format_types,
                        visited=visited.copy()
                    )

        return result

    @classmethod
    def from_dict(
        cls: Any,
        data: Dict[str, Any],
        exclude: Set[str] = None,
        type_converters: Dict[Type, Callable[[Any], Any]] = None,
        visited: Set[int] = None
    ):
        """
        从字典创建 ORM 模型实例

        Args:
            data: 要转换的字典数据
            exclude: 要排除的属性名集合
            type_converters: 类型转换函数字典，如 {str: lambda x: x.strip()}
            visited: 防止循环引用的已访问对象集合（内部使用）

        Returns:
            创建的 ORM 模型实例
        """
        if exclude is None:
            exclude = set()

        if type_converters is None:
            type_converters = _g_type_converters

        if visited is None:
            visited = set()

        # mapper: Mapper = inspect(cls)
        mapper = class_mapper(cls)
        kwargs = {}

        # 处理普通列
        for column in mapper.columns:
            if column.key in exclude or column.key not in data:
                continue

            # 应用类型转换
            value = data[column.key]
            converter = type_converters.get(type(column.type))
            if converter:
                value = converter(value)
            # for type_, converter in type_converters.items():
            #     if isinstance(column.type, type_):
            #         value = converter(value)
            #         break
            kwargs[column.key] = value

        # 处理关系属性
        for rel in mapper.relationships:
            if rel.key in exclude or rel.key not in data:
                continue

            rel_data = data[rel.key]

            if rel_data is None:
                kwargs[rel.key] = None
            elif isinstance(rel, RelationshipProperty):
                if rel.uselist:  # 一对多或多对多关系
                    kwargs[rel.key] = [
                        rel.mapper.class_.from_dict(
                            item_data,
                            exclude=exclude,
                            type_converters=type_converters,
                            visited=visited.copy()
                        )
                        for item_data in rel_data
                    ]
                else:  # 多对一或一对一关系
                    kwargs[rel.key] = rel.mapper.class_.from_dict(
                        rel_data,
                        exclude=exclude,
                        type_converters=type_converters,
                        visited=visited.copy()
                    )

        # 创建实例
        instance = cls(**kwargs)
        return instance

    def compare(self, other, include_keys=None, exclude_keys=None):
        """
        支持与同类型对象比较，可以指定包含和排除的字段

        :param other: 要比较的同类型对象
        :param include_keys: 要包含比较的字段列表
        :param exclude_keys: 要排除比较的字段列表
        :return: 如果对象相等返回 True，否则返回 False
        """
        if not isinstance(other, type(self)):
            return False

        mapper = class_mapper(self.__class__)
        # 过滤出普通列，不包含 relationship 字段
        all_columns = [prop.key for prop in mapper.iterate_properties
                       if isinstance(prop, ColumnProperty)]

        if include_keys:
            columns_to_compare = [
                col for col in all_columns if col in include_keys]
        else:
            columns_to_compare = all_columns

        if exclude_keys:
            columns_to_compare = [
                col for col in columns_to_compare if col not in exclude_keys]

        for column in columns_to_compare:
            self_value = getattr(self, column)
            other_value = getattr(other, column)
            if self_value != other_value:
                return False
        return True


class ModelBase(Base, ModelMixin):
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime, default=datetime.datetime.now)
    updated_at = sa.Column(
        sa.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)


"""
- eq: == 等于
- ne: != 不等于
- gt: >  大于
- lt: <  小于
- ge: >= 大于等于
- le: <= 小于等于
- in:    包含在列表中
- like:  模糊匹配(支持%和_通配符)
- isnull: 是否为None (值应为True/False)
"""
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
                raise ValueError("OR condition need array")
            return or_(*[dict_to_sa_filter(model, sub) for sub in value])

        elif key_lower == "and":
            if not isinstance(value, list):
                raise ValueError("AND condition need array")
            return and_(*[dict_to_sa_filter(model, sub) for sub in value])

        elif key_lower == "not":
            if not isinstance(value, dict):
                raise ValueError("NOT condition need dict")
            return not_(dict_to_sa_filter(model, value))

        # 处理字段条件
        else:
            if "__" in key:
                field_name, operator = key.split("__", 1)
            else:
                field_name, operator = key, "eq"

            column = getattr(model, field_name, None)
            if not column:
                raise AttributeError(f"'{field_name}' not in model: {model}")

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
                    raise ValueError("isnull condition need True/False")
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
                    raise ValueError("NOT condition need only on dict")
            else:
                raise ValueError(f"operator not support: {operator}")

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

    def execute(self, sql: str, params: dict = None) -> ResultProxy:
        logger.info("sql: %s, params: %s", sql, params)
        with self.session() as sess:
            result: ResultProxy = sess.execute(text(sql), params or {})
            sess.commit()
        return result

    def select(self, sql: str, params: dict = None) -> List[Dict[str, Any]]:
        """
        执行SQL查询并返回字典列表，select语句中不能有重复的字段
        :param sql: SQL查询语句
        :param params: 查询参数
        :return: 字典列表
        """
        logger.info("sql: %s, params: %s", sql, params)

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
            logger.error("query failed: %s", e)

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
    from pylibx import utils

    utils.log_base_config()
    DATABASE_URL = "mysql+pymysql://test:test@dev.local:3306/test"
    db_cli = DBClient(connection=DATABASE_URL)
    res = db_cli.select("select * from users limit 3;")
    print_pretty_table(res)


if __name__ == "__main__":
    _main()
