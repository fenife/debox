import pytest
from datetime import datetime
from pylibx.dict_list_util import filter_dict_list, dict_compare


@pytest.fixture
def sample_data():
    return [
        {"id": 1, "name": "Alice", "age": 25, "active": True, "email": "alice@example.com", "tags": ["admin", "user"], "created_at": datetime(2023, 1, 1)},
        {"id": 2, "name": "Bob", "age": 30, "active": False, "email": "bob@test.org", "tags": ["user"], "created_at": datetime(2023, 1, 2)},
        {"id": 3, "name": "Charlie", "age": 35, "active": True, "email": "charlie@example.net", "tags": None, "created_at": None},
        {"id": 4, "name": "David", "age": None, "active": True, "email": "DAVID@example.com", "tags": ["admin"], "created_at": datetime(2023, 1, 3)},
    ]

class TestDictListFilter(object):
    def test_basic_filter(self, sample_data):
        # 测试基本等于条件
        result = filter_dict_list(sample_data, {"name__eq": "Alice"})
        assert len(result) == 1
        assert result[0]["id"] == 1

    def test_comparison_operators(self, sample_data):
        # 测试比较操作符
        result = filter_dict_list(sample_data, {"age__gt": 28})
        assert len(result) == 2
        assert {item["id"] for item in result} == {2, 3}

        result = filter_dict_list(sample_data, {"age__le": 30})
        assert len(result) == 2
        assert {item["id"] for item in result} == {1, 2}

    def test_like_operator(self, sample_data):
        # 测试like操作符
        result = filter_dict_list(sample_data, {"email__like": "%example%"})
        assert len(result) == 3
        assert {item["id"] for item in result} == {1, 3, 4}

        result = filter_dict_list(sample_data, {"email__like": "%.com"})
        assert len(result) == 2
        assert {item["id"] for item in result} == {1, 4}

    def test_isnull_operator(self, sample_data):
        # 测试isnull操作符
        result = filter_dict_list(sample_data, {"tags__isnull": True})
        assert len(result) == 1
        assert result[0]["id"] == 3

        result = filter_dict_list(sample_data, {"created_at__isnull": False})
        assert len(result) == 3
        assert {item["id"] for item in result} == {1, 2, 4}

    def test_in_operator(self, sample_data):
        # 测试in操作符
        result = filter_dict_list(sample_data, {"name__in": ["Alice", "Bob"]})
        assert len(result) == 2
        assert {item["id"] for item in result} == {1, 2}

    def test_in_operator(self, sample_data):
        # 测试contains操作符
        result = filter_dict_list(sample_data, {"tags__contains": "admin"})
        assert len(result) == 2
        assert {item["id"] for item in result} == {1, 4}

    def test_case_sensitive(self, sample_data):
        # 测试大小写敏感
        result = filter_dict_list(sample_data, {"email__eq": "DAVID@example.com"}, case_sensitive=True)
        assert len(result) == 1
        assert result[0]["id"] == 4

        result = filter_dict_list(sample_data, {"email__eq": "david@example.com"}, case_sensitive=False)
        assert len(result) == 1
        assert result[0]["id"] == 4

    def test_logical_operators(self, sample_data):
        # 测试AND条件
        result = filter_dict_list(sample_data, {
            "and": [
                {"age__gt": 25},
                {"active": True}
            ]
        })
        assert len(result) == 1
        assert result[0]["id"] == 3

        # 测试OR条件
        result = filter_dict_list(sample_data, {
            "or": [
                {"name__eq": "Alice"},
                {"name__eq": "Bob"}
            ]
        })
        assert len(result) == 2
        assert {item["id"] for item in result} == {1, 2}

        # 测试NOT条件
        result = filter_dict_list(sample_data, {
            "not": {"active": True}
        })
        assert len(result) == 1
        assert result[0]["id"] == 2

    def test_complex_conditions(self, sample_data):
        # 测试复杂组合条件
        result = filter_dict_list(sample_data, {
            "or": [
                {
                    "and": [
                        {"age__lt": 30},
                        {"active": True}
                    ]
                },
                {
                    "and": [
                        {"email__like": "%example.net"},
                        {"name__contains": "arl"}
                    ]
                }
            ]
        })
        assert len(result) == 2
        assert {item["id"] for item in result} == {1, 3}

    def test_empty_filters(self, sample_data):
        # 测试空过滤条件
        result = filter_dict_list(sample_data, {})
        assert len(result) == len(sample_data)

    def test_invalid_operator(self, sample_data):
        # 测试无效操作符
        with pytest.raises(ValueError, match="不支持的操作符"):
            filter_dict_list(sample_data, {"name__invalid": "Alice"})

    def test_invalid_isnull_value(self, sample_data):
        # 测试无效的isnull值
        with pytest.raises(ValueError, match="isnull操作符需要布尔值"):
            filter_dict_list(sample_data, {"tags__isnull": "yes"})


class TestDictCompare(object):
    def test_dict_compare_all_none(self):
        dict1 = dict2 = None
        result = dict_compare(dict1, dict2)
        assert result is False

    def test_dict_compare_none_empty(self):
        dict1 = None
        dict2 = {}
        result = dict_compare(dict1, dict2)
        assert result is False

    def test_dict_compare_all_empty(self):
        dict1 = dict2 = {}
        result = dict_compare(dict1, dict2)
        assert result is True

    def test_dict_compare_one_empty(self):
        dict1 = {}
        dict2 = {"a": 1}
        result = dict_compare(dict1, dict2)
        assert result is False

    def test_dict_compare_all_keys_equal(self):
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'a': 1, 'b': 2}
        result = dict_compare(dict1, dict2)
        assert result is True

    def test_dict_compare_all_keys_not_equal(self):
        dict1 = {'a': 1, 'b': 2}
        dict2 = {'a': 1, 'b': 3}
        result = dict_compare(dict1, dict2)
        assert result is False

    def test_dict_compare_include_keys_equal(self):
        dict1 = {'a': 1, 'b': 2, 'c': 3}
        dict2 = {'a': 1, 'b': 2, 'c': 4}
        result = dict_compare(dict1, dict2, include_keys=['a', 'b'])
        assert result is True

    def test_dict_compare_include_keys_not_equal(self):
        dict1 = {'a': 1, 'b': 2, 'c': 3}
        dict2 = {'a': 1, 'b': 4, 'c': 3}
        result = dict_compare(dict1, dict2, include_keys=['a', 'b'])
        assert result is False

    def test_dict_compare_exclude_keys_equal(self):
        dict1 = {'a': 1, 'b': 2, 'c': 3}
        dict2 = {'a': 1, 'b': 2, 'c': 4}
        result = dict_compare(dict1, dict2, exclude_keys=['c'])
        assert result is True

    def test_dict_compare_exclude_keys_not_equal(self):
        dict1 = {'a': 1, 'b': 2, 'c': 3}
        dict2 = {'a': 1, 'b': 4, 'c': 3}
        result = dict_compare(dict1, dict2, exclude_keys=['c'])
        assert result is False
