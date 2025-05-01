import pandas as pd
import pytest
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pylibx import db_util
from test_models import User, Article, Category, Base

# 测试用的内存SQLite数据库
TEST_DB_URL = "sqlite:///:memory:"

@pytest.fixture(scope="module")
def setup_database():
    """初始化测试数据库和表结构"""
    _db_cli = db_util.DBClient(TEST_DB_URL)

    # 创建表
    # Base.metadata.create_all(_db_cli.engine)
    User.__table__.create(_db_cli.engine)
    Category.__table__.create(_db_cli.engine)
    Article.__table__.create(_db_cli.engine)
    
    # 插入测试数据
    user1 = User(
        id=1,
        name="Alice",
        created_at=datetime(2023, 1, 1, 10, 0, 0),
        status="active"
    )
    user2 = User(
        id=2,
        name="Bob",
        created_at=datetime(2023, 1, 2, 11, 0, 0),
        status="inactive"
    )
    
    category1 = Category(
        id=1,
        name="Technology",
        created_at=datetime(2023, 1, 5, 9, 0, 0),
        user_id=1
    )
    category2 = Category(
        id=2,
        name="Science",
        created_at=datetime(2023, 1, 6, 10, 0, 0),
        user_id=2
    )
    
    article1 = Article(
        id=1,
        title="Python 3.11 New Features",
        content="...",
        created_at=datetime(2023, 1, 10, 12, 0, 0),
        user_id=1,
        category_id=1
    )
    article2 = Article(
        id=2,
        title="Quantum Computing Advances",
        content="...",
        created_at=datetime(2023, 1, 15, 13, 0, 0),
        user_id=1,
        category_id=2
    )
    article3 = Article(
        id=3,
        title="Climate Change Research",
        content="...",
        created_at=datetime(2023, 1, 20, 14, 0, 0),
        user_id=2,
        category_id=2
    )
    
    # with _db_cli.engine.connect() as conn:
    with _db_cli.session() as sess:
        sess.add_all([user1, user2, category1, category2, article1, article2, article3])
        sess.commit()

        all_users = sess.query(User).all()
        for user in all_users:
            print(user.name)
    
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
        a.id as article_id,
        a.title,
        a.created_at as article_created
    FROM users u
    JOIN articles a ON u.id = a.user_id
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

