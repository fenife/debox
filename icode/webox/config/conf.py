from config import conf_local
from config import conf_dev


_vm_configs = {
    "shell": {
        "local": {
            "name": "local",
            "host": "127.0.0.1",
            "port": 22,
            "user": "feng",
            "passwd": "123",
        },
        "vmc1": {
            "name": "vmc1",
            "host": "172.18.0.2",
            "port": 22,
            "user": "root",
            "passwd": "r123",
        }
    }
}

_env_configs = {
    "local": conf_local.configs,
    "dev": conf_dev.configs,
}


def get_env_configs(env: str):
    configs = _env_configs.get(env, {})
    if not configs:
        raise Exception(f"configs not found, env: {env}")
    configs.update(_vm_configs)
    return configs


def get_db_conf(env: str):
    configs = get_env_configs(env)
    return configs.get("bos", {}).get("db")


def get_server_conf(env: str):
    configs = get_env_configs(env)
    return configs.get("bos", {}).get("server")

def get_shell_conf(env: str, vm_name: str):
    configs = get_env_configs(env)
    return configs.get("shell", {}).get(vm_name)
