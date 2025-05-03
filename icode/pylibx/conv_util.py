from dataclasses import asdict, is_dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Type, TypeVar, Optional
import json

T = TypeVar('T')

class DataclassMixin:
    """为dataclass添加字典和JSON转换功能的Mixin"""
    
    def to_dict(self) -> Dict[str, Any]:
        """将dataclass对象转换为字典"""
        def convert(value: Any):
            if isinstance(value, datetime):
                return value.isoformat()
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
            if field_type is datetime:
                return datetime.fromisoformat(value)
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
