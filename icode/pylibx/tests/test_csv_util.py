import csv
import os
import pytest
from tempfile import NamedTemporaryFile
from pylibx import csv_util
from pylibx.csv_util import write_dict_list_to_csv, read_csv_to_dict_list

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


class TestWriteDictListToCSV:
    @pytest.fixture
    def sample_data(self):
        return [
            {'name': 'Alice', 'age': 25, 'city': 'New York'},
            {'name': 'Bob', 'age': 30, 'city': 'Los Angeles'},
            {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}
        ]

    @pytest.fixture
    def sample_fieldnames(self):
        return ['name', 'age', 'city']

    def test_write_dict_list_to_csv(self, sample_data, sample_fieldnames):
        with NamedTemporaryFile(mode='w+', newline='', encoding='utf-8', delete=True) as f:
            file_path = f.name
            write_dict_list_to_csv(sample_data, file_path, sample_fieldnames)
            f.seek(0)
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == len(sample_data) + 1
            assert rows[0] == sample_fieldnames
            for i, row in enumerate(rows[1:]):
                for field, value in zip(sample_fieldnames, row):
                    assert str(sample_data[i][field]) == value

    def test_write_dict_list_to_csv_append_mode(self, sample_data, sample_fieldnames):
        with NamedTemporaryFile(mode='w+', newline='', encoding='utf-8', delete=True) as f:
            file_path = f.name
            write_dict_list_to_csv(sample_data, file_path, sample_fieldnames, mode='w')
            write_dict_list_to_csv(sample_data, file_path, sample_fieldnames, mode='a')
            f.seek(0)
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) == len(sample_data) * 2 + 1
            assert rows[0] == sample_fieldnames
            for i, row in enumerate(rows[1:len(sample_data)+1]):
                for field, value in zip(sample_fieldnames, row):
                    assert str(sample_data[i][field]) == value
            for i, row in enumerate(rows[len(sample_data)+1:]):
                for field, value in zip(sample_fieldnames, row):
                    assert str(sample_data[i][field]) == value


class TestReadCSVToDictList:
    @pytest.fixture
    def sample_data(self):
        return [
            {'name': 'Alice', 'age': '25', 'city': 'New York'},
            {'name': 'Bob', 'age': '30', 'city': 'Los Angeles'},
            {'name': 'Charlie', 'age': '35', 'city': 'Chicago'}
        ]

    def test_read_csv_to_dict_list(self, sample_data):
        with NamedTemporaryFile(mode='w+', newline='', encoding='utf-8', delete=True) as f:
            fieldnames = sample_data[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in sample_data:
                writer.writerow(row)
            f.seek(0)
            result = read_csv_to_dict_list(f.name)
            assert len(result) == len(sample_data)
            for i in range(len(result)):
                for key in result[i].keys():
                    assert result[i][key] == sample_data[i][key]
