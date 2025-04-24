
import sqlalchemy as sa
from sqlalchemy import or_, and_, not_, ColumnElement
from sqlalchemy.orm import Query
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.dialects import mysql
from typing import Dict, Any, Union, List
from sqlalchemy import not_, or_, and_, ColumnElement
from typing import Dict, Any, Union, List

def dict_to_sqlalchemy_filter(
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
            return or_(*[dict_to_sqlalchemy_filter(model, sub) for sub in value])
            
        elif key_lower == "and":
            if not isinstance(value, list):
                raise ValueError("AND 条件需要数组格式")
            return and_(*[dict_to_sqlalchemy_filter(model, sub) for sub in value])
            
        elif key_lower == "not":
            if not isinstance(value, dict):
                raise ValueError("NOT 条件需要字典格式")
            return not_(dict_to_sqlalchemy_filter(model, value))

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
                    negated_op = {
                        "eq": "ne",
                        "ne": "eq",
                        "gt": "le",
                        "lt": "ge",
                        "ge": "lt",
                        "le": "gt",
                        "like": "notlike",
                        "in": "notin"
                    }.get(sub_op, sub_op)
                    clauses.extend(
                        dict_to_sqlalchemy_filter(
                            model, 
                            {f"{field_name}__{negated_op}": sub_val}
                        )
                    )
                else:
                    raise ValueError("NOT 操作符需要单个条件字典")
            else:
                raise ValueError(f"不支持的运算符: {operator}")

    return and_(*clauses) if clauses else None

def build_query(
    model: Any,
    filters: Dict[str, Any],
    query: Query = None
) -> Query:
    """
    构建带过滤条件的查询
    """
    query = query or session.query(model)
    condition = dict_to_sqlalchemy_filter(model, filters)
    if condition is not None:
        return query.filter(condition)
    return query


# 等效于 WHERE age > 18 AND status = 'active'
filter_dict = {
    "age__gt": 18,
    "status": "active"
}

# 等效于 WHERE name = 'John' OR email LIKE '%@example.com'
filter_dict = {
    "or": [
        {"name": "John"},
        {"email__like": "%@example.com"}
    ]
}

# 等效于 WHERE (age >= 65 OR is_retired = true) AND country IN ('US', 'CA')
filter_dict = {
    "and": [
        {
            "or": [
                {"age__ge": 65},
                {"is_retired": True}
            ]
        },
        {
            "country__in": ["US", "CA"]
        }
    ]
}

# 等效于 WHERE (role = 'admin' AND status != 'disabled') 
#        OR (is_superuser = true AND last_login > '2023-01-01')
filter_dict = {
    "or": [
        {
            "and": [
                {"role": "admin"},
                {"status__ne": "disabled"}
            ]
        },
        {
            "and": [
                {"is_superuser": True},
                {"last_login__gt": "2023-01-01"}
            ]
        }
    ]
}

"""
# 基础空值查询
# IS NULL
{"email__isnull": True}
# WHERE email IS NULL

# IS NOT NULL 
{"email__isnull": False}
# WHERE email IS NOT NULL

# 字段级 NOT 操作
# NOT EQUAL
{"age__not": {"eq": 18}}
# WHERE age != 18

# NOT LIKE
{"name__not": {"like": "%test%"}}
# WHERE name NOT LIKE '%test%'

# NOT IN
{"id__not": {"in": [1,2,3]}}
# WHERE id NOT IN (1, 2, 3)
"""

filter_dict = {
    "not": {
        "or": [
            {"status__isnull": True},
            {"and": [
                {"age__gt": 65},
                {"is_retired": False}
            ]}
        ]
    }
}
# WHERE NOT (
#     status IS NULL 
#     OR (age > 65 AND is_retired = false)
# )

# 创建 declarative base 类
Base = declarative_base()

class User(Base):
    """用户表模型"""
    __tablename__ = "users"  # 数据库表名

    # 定义字段（主键自动生成）
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), nullable=False)  # 字符串类型，长度限制50，非空
    age = sa.Column(sa.Integer)
    city = sa.Column(sa.String(100), default="Unknown")  # 默认值

# 使用示例
query = build_query(User, filter_dict)
results = query.all()
