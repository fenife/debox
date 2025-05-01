
import pytest
from datetime import datetime
from sqlalchemy import create_engine, text
from pylibx import db_util
import pandas as pd

# 测试用的内存SQLite数据库
TEST_DB_URL = "sqlite:///:memory:"


@pytest.fixture(scope="module")
def setup_database():
    """初始化测试数据库"""
    _db_cli = db_util.DBClient(TEST_DB_URL)

    with _db_cli.engine.connect() as conn:
        # 创建测试表
        conn.execute(text("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT,
            created_at DATETIME,
            status TEXT
        )"""))

        conn.execute(text("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            amount REAL,
            created_at DATETIME,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )"""))

        # 插入测试数据
        conn.execute(text("""
        INSERT INTO users (id, name, created_at, status)
        VALUES
            (1, 'Alice', '2023-01-01 10:00:00', 'active'),
            (2, 'Bob', '2023-01-02 11:00:00', 'inactive')
        """))

        conn.execute(text("""
        INSERT INTO orders (id, user_id, amount, created_at)
        VALUES
            (1, 1, 100.5, '2023-01-10 12:00:00'),
            (2, 1, 200.0, '2023-01-15 13:00:00'),
            (3, 2, 50.0, '2023-01-20 14:00:00')
        """))
        conn.commit()

    yield _db_cli

    # 测试结束后清理
    _db_cli.engine.dispose()


@pytest.fixture
def _db_cli(setup_database):
    cli = setup_database
    return cli


def test_execute_sql_with_join(_db_cli):
    """测试多表关联查询"""
    sql = """
    SELECT
        u.id as user_id,
        u.name,
        u.created_at as user_created,
        o.id as order_id,
        o.amount,
        o.created_at as order_created
    FROM users u
    JOIN orders o ON u.id = o.user_id
    WHERE u.status = :status
    """

    data = _db_cli.select(sql, {"status": "active"})
    # 验证返回结果
    assert len(data) == 2
    assert isinstance(data[0]["user_created"], str)  # 验证日期转为字符串


def test_empty_result(_db_cli):
    """测试空结果集"""
    sql = "SELECT * FROM users WHERE status = 'nonexistent'"
    data = _db_cli.select(sql)
    assert len(data) == 0


def test_to_dataframe(_db_cli):
    """测试转换为DataFrame"""
    sql = "SELECT id, name FROM users"
    data = _db_cli.select(sql)
    df = db_util.to_dataframe(data)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 2
    assert "id" in df.columns
    assert "name" in df.columns


def test_pretty_table_output(_db_cli, capsys):
    """测试PrettyTable输出"""
    sql = "SELECT id, name FROM users LIMIT 1"
    data = _db_cli.select(sql)
    db_util.print_pretty_table(data)
    captured = capsys.readouterr()
    assert "id" in captured.out
    assert "name" in captured.out
    assert "Alice" in captured.out or "Bob" in captured.out
    print(captured.out)
