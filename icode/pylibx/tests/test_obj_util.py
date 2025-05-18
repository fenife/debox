import pytest
from datetime import datetime
from enum import Enum
import numpy as np
import pandas as pd
from typing import List, Optional
from dataclasses import dataclass, field
from pylibx.obj_util import DataclassMixin, df_to_objs
from pylibx import dict_util


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass
class Address(DataclassMixin):
    street: str
    city: str
    zip_code: str


@dataclass
class Customer(DataclassMixin):
    id: int
    name: str
    status: Status
    join_date: datetime
    address: Address
    tags: list[str] = field(default_factory=list)


@dataclass
class Person:
    name: str
    age: Optional[int] = None
    city: Optional[str] = None


class TestDataclassMixinConversion:
    def test_dataclass_conversion(self):
        # 创建测试对象
        address = Address(street="123 Main St",
                          city="New York", zip_code="10001")
        customer = Customer(
            id=1,
            name="Alice",
            status=Status.ACTIVE,
            join_date=datetime(2023, 1, 1),
            address=address,
            tags=["vip", "early-adopter"]
        )

        # 测试对象转字典
        customer_dict = customer.to_dict()
        assert customer_dict["name"] == "Alice"
        assert customer_dict["status"] == "active"
        assert isinstance(customer_dict["join_date"], str)
        assert customer_dict["address"]["city"] == "New York"

        # 测试字典转对象
        new_customer = Customer.from_dict(customer_dict)
        assert new_customer.id == 1
        assert new_customer.status == Status.ACTIVE
        assert new_customer.join_date == datetime(2023, 1, 1)
        assert isinstance(new_customer.address, Address)

        # 测试对象转JSON
        customer_json = customer.to_json()
        assert '"name": "Alice"' in customer_json
        assert '"status": "active"' in customer_json

        # 测试JSON转对象
        loaded_customer = Customer.from_json(customer_json)
        assert loaded_customer.name == "Alice"
        assert loaded_customer.address.street == "123 Main St"

    def test_edge_cases(self):
        # 测试None值处理
        @dataclass
        class TestNone(DataclassMixin):
            value: str | None

        obj = TestNone(value=None)
        assert obj.to_dict()["value"] is None
        assert TestNone.from_dict({"value": None}).value is None

        # 测试空列表
        @dataclass
        class TestList(DataclassMixin):
            items: list[str]

        obj = TestList(items=[])
        assert obj.to_dict()["items"] == []
        assert TestList.from_dict({"items": []}).items == []


@dataclass
class CustomData(DataclassMixin):
    field1: int
    field2: str
    field3: bool

@pytest.fixture
def obj1():
    return CustomData(field1=1, field2="test", field3=True)

@pytest.fixture
def obj2():
    return CustomData(field1=1, field2="test", field3=True)

@pytest.fixture
def obj3():
    return CustomData(field1=2, field2="test", field3=True)


class TestDataclassMixinCompare:

    def test_equal_without_filters(self, obj1, obj2):
        assert obj1.comapre(obj2)

    def test_not_equal_without_filters(self, obj1, obj3):
        assert not obj1.comapre(obj3)

    def test_equal_with_include_keys(self, obj1, obj3):
        assert obj1.comapre(obj3, include_keys=["field2", "field3"])

    def test_not_equal_with_exclude_keys(self, obj1, obj3):
        assert not obj1.comapre(obj3, exclude_keys=["field2", "field3"])


class TestDataFrameToDataclassList:
    def test_empty_df(self):
        df = pd.DataFrame()
        result = df_to_objs(df, Person)
        assert result == []

    def test_single_row(self):
        df = pd.DataFrame({'name': ['Alice'], 'age': [30], 'city': ['New York']})
        result = df_to_objs(df, Person)
        assert len(result) == 1
        assert isinstance(result[0], Person)
        assert result[0].name == 'Alice'
        assert result[0].age == 30
        assert result[0].city == 'New York'

    def test_multiple_rows(self):
        df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'age': [30, 25],
            'city': ['New York', 'London']
        })
        result = df_to_objs(df, Person)
        assert len(result) == 2
        assert result[0].name == 'Alice'
        assert result[1].age == 25

    def test_with_nan_values(self):
        df = pd.DataFrame({
            'name': ['Alice', 'Bob'],
            'age': [30, np.nan],
            'city': [np.nan, 'London']
        })
        result = df_to_objs(df, Person)
        assert result[0].age == 30
        assert result[0].city is None
        assert result[1].age is None
        assert result[1].city == 'London'

    def test_missing_required_field(self):
        # 缺少必需字段'name'
        df = pd.DataFrame({'age': [30]})  
        objs = df_to_objs(df, Person)
        assert objs[0].name == None

    def test_extra_columns_in_df(self):
        df = pd.DataFrame({
            'name': ['Alice'],
            'age': [30],
            'city': ['New York'],
            'extra': ['value']  # 额外列
        })
        result = df_to_objs(df, Person)
        assert result[0].name == 'Alice'
        assert not hasattr(result[0], 'extra')    
