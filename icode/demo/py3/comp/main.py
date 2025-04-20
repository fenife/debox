import json
import csv
import os
from loguru import logger
from prettytable import PrettyTable


def create_path(file_path):
    if not os.path.exists(file_path):
        os.mkdir(file_path)
        logger.info("create path: {}", file_path)


def create_demo_data():
    def write_csv_data(filename, data):
        create_path('./data')
        # 写入 CSV 文件
        with open(filename, 'w', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'age', 'city']
            csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            csv_writer.writeheader()  # 写入标题行
            csv_writer.writerows(data)  # 写入多行数据

    # 要写入的数据（字典格式）
    data1 = [
        {'id': 1, 'name': 'Alice', 'age': 30, 'city': 'New York'},
        {'id': 2, 'name': 'Bob', 'age': 25, 'city': 'London'},
        {'id': 4, 'name': 'Charlie', 'age': 35, 'city': 'Paris'}
    ]

    data2 = [
        {'id': 1, 'name': 'Alice', 'age': 30, 'city': 'New York'},
        {'id': 3, 'name': 'John', 'age': 28, 'city': 'London'},
        {'id': 4, 'name': 'Charlie', 'age': 36, 'city': 'paris'}
    ]

    write_csv_data('./data/data1.csv', data1)
    write_csv_data('./data/data2.csv', data2)


def read_csv_data(filename: str):
    dict_rows = []
    with open(filename, 'r', encoding='utf-8') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            # print(row['列名1'], row['列名2'])  # 通过列名访问数据
            dict_rows.append(row)
    return dict_rows


class RecordAuditor(object):
    def __init__(self, dict_rows1, dict_rows2):
        self.data1_dict = {str(item['id']): item for item in dict_rows1}
        self.data2_dict = {str(item['id']): item for item in dict_rows2}

    def compare_data(self):
        compare_keys = ['name', 'age', 'city']
        # 以dict1为准，新增，删除、不同的分别计算得出
        # dict1 = {item['id']: item for item in self.data1}
        # dict2 = {item['id']: item for item in self.data2}
        dict1 = self.data1_dict
        dict2 = self.data2_dict
        
        ids1 = set(dict1.keys())
        ids2 = set(dict2.keys())

        added_ids = ids2 - ids1
        deleted_ids = ids1 - ids2
        modified_ids = set()
        common_ids = ids1 & ids2
        for data_id in common_ids:
            record1 = dict1[data_id]
            record2 = dict2[data_id]
            for key in compare_keys:
                if record1.get(key) != record2.get(key):
                    modified_ids.add(data_id)
        return {'added': added_ids, 'deleted': deleted_ids, 'modified': modified_ids}

    def print_pretty_result(self, result):

        def add_dict_row(table, row_dict):
            # 确保字典键与表格字段一致，缺失字段填充为空
            row = [row_dict.get(field, "") for field in table.field_names]
            table.add_row(row)

        logger.info(self.data1_dict)
        logger.info(self.data2_dict)
        logger.info(result)

        table = PrettyTable()
        table.field_names = ["id", "name", "age", "city", "old", "new"]
        added_ids = result.get('added', set())
        deleted_ids = result.get('deleted', set())
        modified_ids = result.get('modified', set())
        # 打印新增数据
        for data_id in added_ids:
            row = self.data2_dict.get(data_id, {})
            row['old'] = 'no'
            row['new'] = 'yes'
            add_dict_row(table, row)

         # 打印删除数据
        for data_id in deleted_ids:
            row = self.data1_dict.get(data_id, {})
            row['old'] = 'yes'
            row['new'] = 'no'
            add_dict_row(table, row)
        
        # 打印修改数据（字段名与其他表格一致，用 → 符号表示变化）
        for data_id in modified_ids:
            # 获取新旧数据
            _old = self.data1_dict.get(data_id)
            _old['old'] = 'yes'
            _old['new'] = 'no'
            add_dict_row(table, _old)

            _new = self.data2_dict.get(data_id)
            _new['old'] = 'no'
            _new['new'] = 'yes'
            add_dict_row(table, _new)

        print(table)
        add_len = len(added_ids)
        del_len = len(deleted_ids)
        mod_len = len(modified_ids)
        print(f"rows len: {len(table.rows)} = add ({add_len}) + del ({del_len}) + mod ({mod_len}) * 2")

    def start(self):
        result = self.compare_data()
        self.print_pretty_result(result)

def main():
    create_demo_data()
    dict_rows1 = read_csv_data('./data/data1.csv')
    dict_rows2 = read_csv_data('./data/data2.csv')
    auditor = RecordAuditor(dict_rows1, dict_rows2)
    auditor.start()


if __name__ == "__main__":
    main()
