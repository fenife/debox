
import yaml


def read_yaml(yaml_path: str, key: str = None):
    with open(yaml_path, encoding='utf-8', mode='r') as f:
        data = yaml.safe_load(f)
    return data if not key else data.get(key)


def write_yaml(yaml_path: str, data):
    with open(yaml_path, encoding='utf-8', mode='w') as f:
        yaml.safe_dump(data, f, allow_unicode=True)


def clean_yaml(yaml_path: str):
    with open(yaml_path, encoding='utf-8', mode='w') as f:
        pass


