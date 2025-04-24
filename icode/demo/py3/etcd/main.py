import os
os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'

import sys
import etcd3
import argparse
from prettytable import PrettyTable


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

def main():
    # 配置命令行参数解析
    parser = argparse.ArgumentParser(description='从etcd获取键值信息')
    parser.add_argument('--host', default='localhost', help='etcd主机地址')
    parser.add_argument('--port', type=int, default=2379, help='etcd端口')
    parser.add_argument('--prefix', required=True, help='要查询的键前缀')
    args = parser.parse_args()

    # 获取数据
    cli = EtcdClient(host=args.host, port=args.port)
    kvs = cli.get_prefix(prefix=args.prefix)

    # 创建并格式化表格
    table = PrettyTable()
    table.field_names = ["Key", "Value", "Revision"]
    table.align["Key"] = "l"
    table.align["Value"] = "l"
    table.align["Revision"] = "r"
    
    for item in kvs:
        # 限制值显示长度避免表格过宽
        trimmed_value = (item["value"][:50] + '...') if len(item["value"]) > 50 else item["value"]
        table.add_row([item["key"], trimmed_value, item["revision"]])
    
    print(table)

if __name__ == "__main__":
    main()
