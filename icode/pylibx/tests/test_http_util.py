import pytest
from datetime import datetime
from pylibx.http_util import HttpClient, HttpResult


@pytest.fixture
def http_cli():
    _cli = HttpClient(host="dev.local", port="8020")
    return _cli


def test_get_category_list(http_cli):
    url = "/api/v1/category/list"
    http_cli.get(url=url)
