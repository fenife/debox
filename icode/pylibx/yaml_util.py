
import pandas as pd
import yaml
import logging

logger = logging.getLogger(__name__)


def read_yaml(yaml_path: str, key: str = None):
    with open(yaml_path, encoding='utf-8', mode='r') as f:
        data = yaml.safe_load(f)
    return data if not key else data.get(key)


def write_yaml(yaml_path: str, data, key: str = None):
    if key:
        data = {key: data}
    with open(yaml_path, encoding='utf-8', mode='w') as f:
        yaml.safe_dump(data, f, allow_unicode=True)


def clean_yaml(yaml_path: str):
    with open(yaml_path, encoding='utf-8', mode='w') as f:
        pass


def read_yaml_to_df(file_path: str) -> pd.DataFrame:
    """读取YAML文件并转换为DataFrame"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    if isinstance(data, list):
        return pd.DataFrame(data)
    elif isinstance(data, dict):
        return pd.DataFrame.from_dict(data, orient='index')
    else:
        raise ValueError(f"unsupport data: {data}")
