import etcd3

class EtcdClient(object):
    def __init__(self, host="localhost", port=2379):
        self.host = host
        self.port = port
        self.etcd_cli = etcd3.client(host=host, port=port)

    def get_prefix(self, prefix='', **kwargs):
        """
        从etcd获取指定前缀的键值及版本信息
        """
        kvs = []
        try:
            # 获取指定前缀的所有键值对
            resp = self.etcd_cli.get_prefix(prefix, **kwargs)
            for value, metadata in resp:
                try:
                    key = metadata.key.decode('utf-8', errors='replace')
                    value_str = value.decode('utf-8', errors='replace')
                    kvs.append({
                        "key": key,
                        "value": value_str,
                        "revision": metadata.mod_revision
                    })
                except Exception as e:
                    print(f"decode failed: {e}, val: {value}")
                    continue
        except Exception as e:
            print(f"etcd get failed: {e}")
        
        return kvs

