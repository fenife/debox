import etcd3
import json
from typing import Callable, List, Union

class EtcdKV:
    def __init__(self, key: str, val: Union[dict, str], revision: int, meta):
        self.key = key
        self.val = val
        self.revision = revision
        self.meta = meta


class EtcdClient(object):
    def __init__(self, host: str = 'localhost', port: int = 2379, **kwargs) -> None:
        self.client = etcd3.client(host=host, port=port, **kwargs)

    def get_prefix(
        self,
        prefix: str,
        key_filter: Callable[[str], bool] = None,
        value_filter: Callable[[Union[dict, str]], bool] = None
    ) -> List[EtcdKV]:
        result: List[EtcdKV] = []
        for value, metadata in self.client.get_prefix(prefix):
            key_str = metadata.key.decode('utf-8')
            try:
                val = json.loads(value.decode('utf-8'))
            except (json.JSONDecodeError, UnicodeDecodeError):
                val = value.decode('utf-8')

            if (key_filter is None or key_filter(key_str)) and (
                    value_filter is None or value_filter(val)):
                kv = EtcdKV(
                    key=key_str,
                    val=val,
                    revision=metadata.mod_revision,
                    meta=metadata
                )
                result.append(kv)
        return result
