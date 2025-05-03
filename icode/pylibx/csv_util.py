import csv
import logging

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

