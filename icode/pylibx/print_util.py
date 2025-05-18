import logging
import pandas as pd
from prettytable import PrettyTable
from typing import Any, Dict, List, Type, TypeVar, Optional, Union


logger = logging.getLogger(__name__)


def print_table_dict_list(
    dict_list: List[Dict[str, Any]],
    columns: List[str] = None,
    max_width: int = 80
):
    """
    使用PrettyTable打印美观的输出
    :param dict_list: 数据字典列表
    :param columns: 指定要显示的列（None表示全部）
    :param max_width: 列最大宽度（自动换行）
    """
    if not dict_list:
        logger.warning("No data to display")
        return

    table = PrettyTable()

    # 确定要显示的列
    display_columns = columns or list(dict_list[0].keys())
    table.field_names = display_columns

    # 设置列格式
    for field in table.field_names:
        table._max_width[field] = max_width
        table.align[field] = "l"

    for row in dict_list:
        table.add_row([row.get(col, '') for col in display_columns])

    print(table)


def print_table_df(
    df: pd.DataFrame,
    max_width: int = 80
):
    """
    使用PrettyTable打印美观的输出
    :param df: dataframe
    :param max_width: 列最大宽度（自动换行）
    """
    if df is None:
        logger.warning("No data to display")
        return

    table = PrettyTable()
    table.field_names = df.columns.tolist()
    table.add_rows(df.values.tolist())  # 批量添加所有行

    # 设置列格式
    for field in table.field_names:
        table._max_width[field] = max_width
        table.align[field] = "l"

    print(table)
