import re
import logging
import pandas as pd
from typing import List, Dict, Any, Union
from datetime import datetime


logger = logging.getLogger(__name__)


def dict_list_to_df(dict_list: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    将字典列表转换为DataFrame
    """
    return pd.DataFrame(dict_list)


def df_to_dict_list(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    将DataFrame转换为字典列表
    """
    if df is None:
        return []
    data = df.to_dict('records')
    return data


def dict_validate(item: Dict[str, Any], condition: Dict[str, Any]) -> bool:
    """
    判断dict的值是否满足条件

    参数:
        item: 要校验的字典
        condition: 校验条件
    返回:
        是否满足条件

    条件语法:
    {
        "field1__op": value,          # 基本条件
        "and": [                       # AND条件
            {"field2__op": value},
            {"field3__op": value}
        ],
        "or": [                        # OR条件
            {"field4__op": value},
            {"field5__op": value}
        ],
        "not": {                       # NOT条件
            "field6__op": value
        }
    }

    支持的操作符(op):
    - eq: 等于 (默认)
    - ne: 不等于
    - gt: 大于
    - lt: 小于
    - ge: 大于等于
    - le: 小于等于
    - in: 包含在列表中
    - like: 模糊匹配(支持%和_通配符)
    - isnull: 是否为None (值应为True/False)
    - contains: 包含子字符串
    - startswith: 以...开头
    - endswith: 以...结尾
    """

    for key, value in condition.items():
        key_lower = key.lower()

        # 处理逻辑运算符
        if key_lower == "and":
            if not isinstance(value, list):
                raise ValueError("AND条件需要数组格式")
            return all(dict_validate(item, cond) for cond in value)

        elif key_lower == "or":
            if not isinstance(value, list):
                raise ValueError("OR条件需要数组格式")
            return any(dict_validate(item, cond) for cond in value)

        elif key_lower == "not":
            if not isinstance(value, dict):
                raise ValueError("NOT条件需要字典格式")
            return not dict_validate(item, value)

        # 处理字段条件
        else:
            if "__" in key:
                field_name, operator = key.rsplit("__", 1)
            else:
                field_name, operator = key, "eq"

            # 获取字段值，需要判断是否过滤的值，不是条件中的值
            if field_name not in item:
                return False
            field_value = item.get(field_name)

            # 大小写不敏感
            if isinstance(field_value, str):
                field_value = field_value.lower()
                if isinstance(value, str):
                    value = value.lower()

            # 应用操作符
            if operator == "eq":
                return field_value == value
            elif operator == "ne":
                return field_value != value
            elif operator == "gt":
                return field_value is not None and value is not None and field_value > value
            elif operator == "lt":
                return field_value is not None and value is not None and field_value < value
            elif operator == "ge":
                return field_value is not None and value is not None and field_value >= value
            elif operator == "le":
                return field_value is not None and value is not None and field_value <= value
            elif operator == "contains":
                if isinstance(field_value, str):
                    return value in field_value
                elif isinstance(field_value, (list, tuple, set)):
                    return value in set(field_value)
                return False
            elif operator == "startswith":
                if not isinstance(field_value, str):
                    return False
                return field_value.startswith(value)
            elif operator == "endswith":
                if not isinstance(field_value, str):
                    return False
                return field_value.endswith(value)
            elif operator == "in":
                if not isinstance(value, (list, tuple, set)):
                    value = [value]
                return field_value in value
            elif operator == "like":
                if not isinstance(field_value, str) or not isinstance(value, str):
                    return False
                # 将SQL LIKE模式转换为正则表达式
                pattern = value.replace('%', '.*').replace('_', '.')
                return re.fullmatch(pattern, field_value) is not None
            elif operator == "isnull":
                if value is True:
                    return field_value is None
                elif value is False:
                    return field_value is not None
                else:
                    raise ValueError("isnull操作符需要布尔值True/False")
            else:
                raise ValueError(f"不支持的操作符: {operator}")

    return True


def filter_dict_list(
    data: List[Dict[str, Any]],
    filters: Dict[str, Any],
    case_sensitive: bool = True
) -> List[Dict[str, Any]]:
    """
    通用字典列表过滤函数

    参数:
        data: 要过滤的字典列表
        filters: 过滤条件字典
        case_sensitive: 是否区分大小写(暂时不支持)

    返回:
        过滤后的字典列表
    """
    if not filters:
        return data.copy()
    return [item for item in data if dict_validate(item, filters)]


def dict_compare(dict1, dict2, include_keys=None, exclude_keys=None):
    """
    对比两个字典，支持指定要对比的 key 列表和排除对比的 key 列表
    两者都是None时，返回False
    两者都是空{}时，返回True
    不支持嵌套字典的对比，只支持单层字典的对比

    :param dict1: 第一个字典
    :param dict2: 第二个字典
    :param include_keys: 要对比的 key 列表，默认为 None 表示对比所有 key
    :param exclude_keys: 要排除对比的 key 列表，默认为 None 表示不排除任何 key
    :return: 如果两个字典在指定规则下相等返回 True，否则返回 False
    """
    if not isinstance(dict1, dict) or not isinstance(dict2, dict):
        return False
    if not dict1 and not dict2:
        # 两个都是空{}，返回True
        return True
    if include_keys is None:
        # 如果未指定要对比的 key 列表，则使用两个字典所有 key 的并集
        all_keys = set(dict1.keys()) | set(dict2.keys())
    else:
        all_keys = set(include_keys)

    if exclude_keys is not None:
        # 从要对比的 key 列表中排除指定的 key
        all_keys = all_keys - set(exclude_keys)

    for key in all_keys:
        if key not in dict1 or key not in dict2:
            return False
        if dict1[key] != dict2[key]:
            return False
    return True


def _test():
    sample_data = [
        {"id": 1, "name": "Alice", "age": 25, "active": True,
         "email": "alice@example.com", "tags": ["admin", "user"],
         "created_at": datetime(2023, 1, 1)},
        {"id": 2, "name": "Bob", "age": 30, "active": False,
         "email": "bob@test.org", "tags": ["user"],
         "created_at": datetime(2023, 1, 2)},
        {"id": 3, "name": "Charlie", "age": 35, "active": True,
         "email": "charlie@example.net", "tags": None, "created_at": None},
        {"id": 4, "name": "David", "age": None, "active": True,
         "email": "DAVID@example.com", "tags": ["admin"],
         "created_at": datetime(2023, 1, 3)},
    ]

    result = filter_dict_list(sample_data, {"name__eq": "Alice"})
    print(result)
    assert len(result) == 1
    assert result[0]["id"] == 1


if __name__ == "__main__":
    _test()
