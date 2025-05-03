import csv
import logging
from typing import List, Dict, Optional, Union


logger = logging.getLogger(__name__)


def read_last_line_as_dict(csv_file):
    """高效读取CSV文件的最后一行并返回字典（第一行是header）"""
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            # 先读取header（第一行）
            header = next(csv.reader(f))

            # 定位到最后一行
            f.seek(0, 2)  # 移动到文件末尾
            pos = f.tell()
            last_line = ""

            # 反向查找最后一个换行符
            while pos > 0:
                pos -= 1
                f.seek(pos)
                char = f.read(1)
                if char == '\n':
                    last_line = f.readline().strip()
                    break

            # 如果没有换行符（单行文件），则读取整个文件
            if not last_line and pos == 0:
                f.seek(0)
                last_line = f.readline().strip()

            # 解析最后一行并转为dict
            if last_line:
                # 处理CSV特殊字符（如逗号、引号）
                values = next(csv.reader([last_line]))
                return dict(zip(header, values))
            else:
                return None  # 空文件
    except Exception as e:
        logger.error("read last line of %s failed: %s" % (csv_file, e))
        data = None
    return data


def read_last_line(csv_file):
    """
    高效读取大文件最后一行（无需加载全部内容）
    从文件末尾开始反向查找最后一行
    """
    try:
        with open(csv_file, 'r', encoding='utf-8') as f:
            # 先读取header（第一行）
            header = next(csv.reader(f))
            # 先将指针移动到文件末尾附近
            f.seek(0, 2)
            # 获取文件大小
            pos = f.tell()
            # 从后往前移动，查找换行符
            while pos > 0:
                pos -= 1
                f.seek(pos)
                if f.read(1) == '\n':
                    break
            # 读取最后一行
            last_line = f.readline()
        data = list(csv.reader([last_line]))[0]
    except Exception as e:
        logger.error("read last line of %s failed: %s" % (csv_file, e))
        data = None
    return data


def write_dict_list_to_csv(
    data: List[Dict],
    file_path: Union[str],
    fieldnames: Optional[List[str]] = None,
    mode: str = 'w'
):
    """
    将字典列表写入 CSV 文件

    :param data: 字典列表，每个字典代表 CSV 文件中的一行
    :param file_path: 要写入的 CSV 文件的路径
    :param fieldnames: CSV 文件的列名列表
    :param mode: 文件打开模式，默认为 'w'（写入）
    """
    if not data:
        return
    logger.info("write to csv file: %s", file_path)
    if not fieldnames:
        fieldnames = data[0].keys()
    try:
        with open(file_path, mode, newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if mode == 'w' or (mode == 'a' and csvfile.tell() == 0):
                writer.writeheader()
            for row in data:
                writer.writerow({field: row.get(field, '') for field in fieldnames})
    except Exception as e:
        logger.error("write to file failed: %s", e)


def read_csv_to_dict_list(file_path):
    """
    读取 CSV 文件并将其内容转换为字典列表

    :param file_path: 要读取的 CSV 文件的路径
    :return: 包含 CSV 文件内容的字典列表
    """
    result = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                result.append(row)
        return result
    except Exception as e:
        logger.error("read csv %s failed: %s", file_path, e)
        return []


def clear_csv_file(file_path):
    """
    清除指定 CSV 文件的内容
    :param file_path: 要清除内容的 CSV 文件的路径
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            # 以写入模式打开文件，不写入任何内容，即可清空文件
            pass
    except Exception as e:
        logger.error("clear csv %s failed: %s", file_path, e)
