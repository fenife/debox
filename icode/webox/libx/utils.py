import inspect


def is_hashable(obj):
    try:
        hash(obj)
        return True
    except TypeError:
        return False


class EnumBase(object):

    @classmethod
    def enums(cls):
        return cls._get_custom_attributes()

    @classmethod
    def _get_custom_attributes(cls):
        attributes = []
        for attr_name, attr_value in cls.__dict__.items():
            # 排除函数、类方法和静态方法
            if inspect.isfunction(attr_value) or \
                isinstance(attr_value, (classmethod, staticmethod)):
                continue
            # 排除以双下划线包围的特殊属性（如__module__）
            if attr_name.startswith('__') or attr_name.endswith('__'):
                continue
            # 跳过不可哈希的值
            if not is_hashable(attr_value):
                continue
            attributes.append(attr_value)
        return attributes


def str2bool(v: str):
    if isinstance(v, bool):
        return v
    if not isinstance(v, str):
        raise ValueError(f"invalid bool value: {v}")

    if v.lower() in ("yes", "true", "True", "t", "y", "1"):
        return True
    elif v.lower() in ("no", "false", "False", "f", "n", "0"):
        return True
    else:
        raise ValueError(f"invalid bool value: {v}")


