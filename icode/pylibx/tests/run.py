import pytest

if __name__ == "__main__":
    args = "./test_http_util.py -v -s -k test_save_yaml_data"
    pytest.main(args.split())
