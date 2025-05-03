import csv
import os
import pytest
from tempfile import NamedTemporaryFile
from pylibx import csv_util

class TestCsvUtilLastLine(object):
    def test_normal_csv(self):
        """测试普通CSV文件"""
        content = "name,age,gender\nAlice,25,F\nBob,30,M"
        with NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(content)
            f.flush()
        
        result = csv_util.read_last_line_as_dict(f.name)
        assert result == {"name": "Bob", "age": "30", "gender": "M"}
        os.unlink(f.name)

    def test_empty_csv(self):
        """测试空文件"""
        with NamedTemporaryFile(mode='w', delete=False) as f:
            pass  # 创建空文件
        
        result = csv_util.read_last_line_as_dict(f.name)
        assert result is None
        os.unlink(f.name)

    def test_single_line_csv(self):
        """测试单行CSV文件"""
        content = "name,age,gender\nAlice,25,F"
        with NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(content)
            f.flush()
        
        result = csv_util.read_last_line_as_dict(f.name)
        assert result == {"name": "Alice", "age": "25", "gender": "F"}
        os.unlink(f.name)

    def test_csv_with_quotes(self):
        """测试包含逗号和引号的CSV"""
        content = 'id,text\n1,"Hello, world!"\n2,"Quote: ""Hi\"\"'
        with NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(content)
            f.flush()
            # print("---123\n", f.read())
        
        result = csv_util.read_last_line_as_dict(f.name)
        assert result == {"id": "2", "text": 'Quote: "Hi"'}
        os.unlink(f.name)
