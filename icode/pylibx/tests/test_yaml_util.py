import os
import pytest
import yaml
from tempfile import NamedTemporaryFile

# 假设你的 YAML 工具函数在 yaml_utils.py 中
from pylibx.yaml_util import read_yaml, write_yaml, clean_yaml


# 测试数据
TEST_DATA = {
    "name": "Test User",
    "age": 30,
    "empty": None,
    "skills": ["Python", "pytest"],
    "nested": {
        "key": "value"
    }
}


class TestYamlUtils:
    @pytest.fixture
    def temp_yaml_file(self):
        """创建一个临时的 YAML 文件用于测试"""
        with NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            yaml.safe_dump(TEST_DATA, f)
            temp_path = f.name
        write_yaml("./data/test_yaml.yaml", TEST_DATA)
        yield temp_path  # 测试使用这个文件
        os.unlink(temp_path)  # 测试完成后删除

    def test_read_yaml(self, temp_yaml_file):
        """测试读取整个 YAML 文件"""
        result = read_yaml(temp_yaml_file)
        assert result == TEST_DATA

    def test_read_yaml_with_key(self, temp_yaml_file):
        """测试读取 YAML 文件的特定键"""
        assert read_yaml(temp_yaml_file, "name") == "Test User"
        assert read_yaml(temp_yaml_file, "skills") == ["Python", "pytest"]
        assert read_yaml(temp_yaml_file, "nested") == {"key": "value"}
        assert read_yaml(temp_yaml_file, "nonexistent") is None
        assert read_yaml(temp_yaml_file, "empty") is None

    def test_write_yaml(self, temp_yaml_file):
        """测试写入 YAML 文件"""
        new_data = {"new": "data"}
        write_yaml(temp_yaml_file, new_data)
        
        # 验证写入的内容
        with open(temp_yaml_file, 'r') as f:
            written_data = yaml.safe_load(f)
        assert written_data == new_data

    def test_write_yaml_with_key(self, temp_yaml_file):
        """测试写入 YAML 文件"""
        new_data = {"new": "data"}
        key="new_key"
        write_yaml(temp_yaml_file, new_data, key=key)

        # 验证写入的内容
        with open(temp_yaml_file, 'r') as f:
            written_data = yaml.safe_load(f)
        assert written_data[key] == new_data

    def test_write_yaml_with_special_chars(self, temp_yaml_file):
        """测试写入包含特殊字符的数据"""
        special_data = {
            "text": "包含中文",
            "special": "!@#$%^&*()",
            "multiline": "line1\nline2"
        }
        write_yaml(temp_yaml_file, special_data)
        
        # 验证写入的内容
        result = read_yaml(temp_yaml_file)
        assert result == special_data

    def test_clean_yaml(self, temp_yaml_file):
        """测试清空 YAML 文件"""
        # 先写入一些数据
        write_yaml(temp_yaml_file, TEST_DATA)
        
        # 清空文件
        clean_yaml(temp_yaml_file)
        
        # 验证文件是否为空
        with open(temp_yaml_file, 'r') as f:
            content = f.read()
        assert content == ""

    def test_read_nonexistent_file(self):
        """测试读取不存在的文件"""
        with pytest.raises(FileNotFoundError):
            read_yaml("nonexistent_file.yaml")

    def test_write_nonexistent_path(self, tmp_path):
        """测试写入到不存在的路径"""
        new_file = tmp_path / "new_dir" / "new_file.yaml"
        with pytest.raises(FileNotFoundError):
            write_yaml(str(new_file), TEST_DATA)

    def test_empty_yaml(self, temp_yaml_file):
        """测试读取空 YAML 文件"""
        clean_yaml(temp_yaml_file)
        assert read_yaml(temp_yaml_file) is None
