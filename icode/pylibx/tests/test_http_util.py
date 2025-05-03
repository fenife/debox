import pytest
from datetime import datetime
from pylibx.http_util import HttpClient
from pylibx import yaml_util
import jsonpath

DATA_YAML_FILE = "./data/data.yaml"


@pytest.fixture
def http_cli():
    _cli = HttpClient(host="dev.local", port="8020")
    return _cli


def test_get_category_list(http_cli):
    url = "/api/v1/category/list"
    http_cli.get(url=url, need_raise=False)


def test_save_yaml_data(http_cli):
    url = "/api/v1/category/list"
    resp = http_cli.get(url=url, need_raise=False)
    if resp:
        data = jsonpath.jsonpath(resp.json(), '$.data')
        yaml_util.write_yaml(DATA_YAML_FILE, data)
