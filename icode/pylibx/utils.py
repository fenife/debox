import os
import inspect
import logging
import sys
from pathlib import Path
from datetime import datetime

LOG_FORMAT = "[%(asctime)s] [%(levelname)4s] [%(name)s:%(lineno)s] -- %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def log_base_config():
    logging.basicConfig(
        level=logging.DEBUG,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )


def setup_logger(
    logger: logging.Logger = logging.root,
    level: str = "info",
    log_file: str = None,
    log_format: str = LOG_FORMAT,
    date_format: str = DATE_FORMAT,
):
    """
    初始化日志配置，同时输出到控制台和文件

    :param log_file: 日志文件路径，None表示不写入文件
    :param console_level: 控制台日志级别
    :param file_level: 文件日志级别
    :param log_format: 日志格式
    :param date_format: 日期格式
    """
    # 清除现有的handler，避免重复日志
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    log_level = getattr(logging, level.upper())
    # 1. 控制台Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter(log_format, datefmt=date_format)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # 2. 文件Handler（如果指定了日志文件）
    if log_file:
        # 确保日志目录存在
        log_path = Path(log_file).parent
        log_path.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(log_format, datefmt=date_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


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


def create_path(file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)
        logger.info("create path: {}", file_path)
