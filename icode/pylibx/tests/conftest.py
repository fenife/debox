import pytest
from pylibx.yaml_util import clean_yaml

DATA_YAML_FILE = "./data/data.yaml"

@pytest.fixture(scope="session", autouse=True)
def clean_data():
    # yield     # 如果有这一行，会在每次执行用例之后清除数据，就看不到用例数据了，不好分析
    clean_yaml(DATA_YAML_FILE)

