import logging
import pandas as pd
from prettytable import PrettyTable
from typing import Any, Dict, List, Type, TypeVar, Optional, Union


logger = logging.getLogger(__name__)


def df_to_orm(df: pd.DataFrame, model: Any):
    if df is None or model is None:
        return None
    columns = model.__table__.columns.keys()
    return [model(**{col: row[col] for col in columns if col in row})
            for _, row in df.iterrows()]


def dict_list_to_df(dict_list: List[Dict[str, Any]]) -> pd.DataFrame:
    """
    将字典列表转换为DataFrame
    """
    return pd.DataFrame(dict_list)


def df_to_dict_list(df: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    将DataFrame转换为字典列表
    """
    if df is None:
        return []
    data = df.to_dict('records')
    return data
