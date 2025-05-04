import json
from dataclasses import asdict, is_dataclass, fields
from datetime import datetime, date
from enum import Enum
from typing import Any, Dict, List, Type, TypeVar, Optional, Union
from pylibx import utils


T = TypeVar('T')


class DataclassMixin:
    """为dataclass添加字典和JSON转换功能的Mixin"""

    def to_dict(self) -> Dict[str, Any]:
        """将dataclass对象转换为字典"""
        def convert(value: Any):
            if isinstance(value, (date, datetime)):
                return utils.format_value(value)
            elif isinstance(value, Enum):
                return value.value
            elif is_dataclass(value):
                return value.to_dict()
            elif isinstance(value, (list, tuple)):
                return [convert(item) for item in value]
            elif isinstance(value, dict):
                return {k: convert(v) for k, v in value.items()}
            return value

        return {k: convert(v) for k, v in asdict(self).items()}

    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """从字典创建dataclass对象"""
        def convert(field_type: Type, value: Any):
            if field_type in (date, datetime):
                return utils.convert_from_value(value, field_type)
            elif isinstance(field_type, type) and issubclass(field_type, Enum):
                return field_type(value)
            elif is_dataclass(field_type):
                return field_type.from_dict(value)
            elif hasattr(field_type, '__origin__'):
                # 处理泛型如List, Optional等
                origin = field_type.__origin__
                args = field_type.__args__

                if origin is list:
                    item_type = args[0]
                    return [convert(item_type, item) for item in value]
                elif origin is dict:
                    key_type, val_type = args
                    return {convert(key_type, k): convert(val_type, v) for k, v in value.items()}
                elif origin is type(Optional):
                    return convert(args[0], value) if value is not None else None
            return value

        field_types = cls.__annotations__
        processed = {
            k: convert(field_types.get(k, type(v)), v)
            for k, v in data.items()
            if k in field_types  # 只处理有类型注解的字段
        }
        return cls(**processed)

    def to_json(self) -> str:
        """将对象转换为JSON字符串"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls: Type[T], json_str: str) -> T:
        """从JSON字符串创建对象"""
        return cls.from_dict(json.loads(json_str))

    def comapre(
        self,
        other: object,
        include_keys: List[str] = None,
        exclude_keys: List[str] = None,
    ) -> bool:
        """
        支持指定包含或排除字段进行对象比较
        :param other: 要比较的另一个对象
        :param include_keys: 要包含比较的字段列表
        :param exclude_keys: 要排除比较的字段列表
        :return: 如果对象相等返回 True，否则返回 False
        """
        if not isinstance(other, type(self)):
            return False

        all_fields = [f.name for f in fields(self)]

        if include_keys:
            fields_to_compare = [
                field for field in all_fields if field in include_keys]
        else:
            fields_to_compare = all_fields

        if exclude_keys:
            fields_to_compare = [
                field for field in fields_to_compare if field not in exclude_keys]

        for field in fields_to_compare:
            self_value = getattr(self, field)
            other_value = getattr(other, field)
            if self_value != other_value:
                return False
        return True
