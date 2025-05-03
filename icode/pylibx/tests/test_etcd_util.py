import pytest
from pylibx.etcd_util import EtcdClient, EtcdKV


@pytest.fixture
def etcd_client():
    return EtcdClient()


def test_get_prefix_without_filters(etcd_client):
    test_key1 = 'test_prefix_key1'
    test_value1 = '{"name": "Alice", "age": 25}'
    test_key2 = 'test_prefix_key2'
    test_value2 = 'regular string'
    etcd_client.client.put(test_key1, test_value1)
    etcd_client.client.put(test_key2, test_value2)

    result = etcd_client.get_prefix('test_prefix_')
    assert len(result) >= 2
    key_value_dict = {kv.key: kv.val for kv in result}
    assert test_key1 in key_value_dict
    assert isinstance(key_value_dict[test_key1], dict)
    assert key_value_dict[test_key1]['name'] == 'Alice'
    assert test_key2 in key_value_dict
    assert key_value_dict[test_key2] == 'regular string'


def test_get_prefix_with_key_filter(etcd_client):
    test_key1 = 'test_prefix_key1'
    test_value1 = '{"name": "Alice", "age": 25}'
    test_key2 = 'test_prefix_key2'
    test_value2 = 'regular string'
    etcd_client.client.put(test_key1, test_value1)
    etcd_client.client.put(test_key2, test_value2)

    def key_filter(key):
        return 'key1' in key

    result = etcd_client.get_prefix('test_prefix_', key_filter=key_filter)
    assert len(result) == 1
    key_value_dict = {kv.key: kv.val for kv in result}
    assert test_key1 in key_value_dict
    assert isinstance(key_value_dict[test_key1], dict)
    assert key_value_dict[test_key1]['name'] == 'Alice'


def test_get_prefix_with_value_filter(etcd_client):
    test_key1 = 'test_prefix_key1'
    test_value1 = '{"name": "Alice", "age": 25}'
    test_key2 = 'test_prefix_key2'
    test_value2 = 'regular string'
    etcd_client.client.put(test_key1, test_value1)
    etcd_client.client.put(test_key2, test_value2)

    def value_filter(value):
        return isinstance(value, dict) and value.get('name') == 'Alice'

    result = etcd_client.get_prefix('test_prefix_', value_filter=value_filter)
    assert len(result) == 1
    key_value_dict = {kv.key: kv.val for kv in result}
    assert test_key1 in key_value_dict
    assert isinstance(key_value_dict[test_key1], dict)
    assert key_value_dict[test_key1]['name'] == 'Alice'


def test_get_prefix_with_both_filters(etcd_client):
    test_key1 = 'test_prefix_key1'
    test_value1 = '{"name": "Alice", "age": 25}'
    test_key2 = 'test_prefix_key2'
    test_value2 = 'regular string'
    etcd_client.client.put(test_key1, test_value1)
    etcd_client.client.put(test_key2, test_value2)

    def key_filter(key):
        return 'key1' in key

    def value_filter(value):
        return isinstance(value, dict) and value.get('name') == 'Alice'

    result = etcd_client.get_prefix('test_prefix_', key_filter=key_filter, value_filter=value_filter)
    assert len(result) == 1
    key_value_dict = {kv.key: kv.val for kv in result}
    assert test_key1 in key_value_dict
    assert isinstance(key_value_dict[test_key1], dict)
    assert key_value_dict[test_key1]['name'] == 'Alice'

    