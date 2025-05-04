import pytest
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from pylibx import db_util
from pylibx.db_util import dict_to_sa_filter, build_query
from test_models import Base, User, Article, Category

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

    # 添加测试数据
    user1 = User(id=1, name='Alice', age=25, is_active=1, status="active")
    user2 = User(id=2, name='Bob', age=30, is_active=0, status="inactive")
    user3 = User(id=3, name='Charlie', age=35, is_active=1, status="active")

    cat1 = Category(id=1, name='Tech')
    cat2 = Category(id=2, name='Science')

    article1 = Article(id=1, title='Python Guide', user_id=1,
                       category_id=1, status='published')
    article2 = Article(id=2, title='SQLAlchemy Tips',
                       user_id=1, category_id=2, status='draft')
    article3 = Article(id=3, title='Advanced Python',
                       user_id=2, category_id=1, status='published')

    # with _db_cli.engine.connect() as conn:
    with _db_cli.session() as sess:
        sess.add_all([user1, user2, user3, cat1, cat2,
                     article1, article2, article3])
        sess.commit()

        # all_users = sess.query(User).all()
        # for user in all_users:
        #     print(user.name)

    yield _db_cli

    # 测试结束后清理
    _db_cli.engine.dispose()


@pytest.fixture(scope="function", autouse=True)
def _db_cli(setup_database):
    cli = setup_database
    return cli


class TestDbClientExecuteCase(object):

    def test_execute_with_params(self, _db_cli):
        sql = "update users set email = 'u1@test.com' where id = :id;"
        params = {"id": 1}
        result = _db_cli.execute(sql, params)

        results = _db_cli.select("select * from users where id = 1;")
        db_util.print_pretty_table(results)
        assert len(results) == 1
        assert results[0].get("email") == 'u1@test.com'


class TestDbClientSelectCase(object):

    def test_select_sql_with_join(self, _db_cli):
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

    def test_empty_result(self, _db_cli):
        """测试空结果集"""
        sql = "SELECT * FROM users WHERE status = 'nonexistent'"
        data = _db_cli.select(sql)
        assert len(data) == 0

    def test_to_dataframe(self, _db_cli):
        """测试转换为DataFrame"""
        sql = "SELECT id, name FROM users"
        data = _db_cli.select(sql)
        df = db_util.to_dataframe(data)
        assert isinstance(df, pd.DataFrame)
        assert df.shape[0] == 3
        assert "id" in df.columns
        assert "name" in df.columns

    def test_pretty_table_output(self, _db_cli, capsys):
        """测试PrettyTable输出"""
        sql = "SELECT id, name FROM users LIMIT 1"
        data = _db_cli.select(sql)
        db_util.print_pretty_table(data)
        captured = capsys.readouterr()
        assert "id" in captured.out
        assert "name" in captured.out
        assert "Alice" in captured.out or "Bob" in captured.out
        print(captured.out)


############################################################
# db client query
############################################################

class TestDBClientQuery(object):

    # 测试用例
    def test_query_basic_filter(self, _db_cli):
        """测试基本过滤条件"""
        results = _db_cli.query(User, filters={'name__eq': 'Alice'})
        assert len(results) == 1
        assert results[0].name == 'Alice'

    def test_query_multiple_conditions(self, _db_cli):
        """测试多条件查询"""
        results = _db_cli.query(User, filters={
            'age__gt': 20,
            'age__lt': 30,
            'is_active': 1
        })
        assert len(results) == 1
        assert results[0].name == 'Alice'

    def test_query_or_condition(self, _db_cli):
        """测试OR条件"""
        results = _db_cli.query(User, filters={
            'or': [
                {'name__eq': 'Alice'},
                {'name__eq': 'Bob'}
            ]
        })
        assert len(results) == 2
        assert {u.name for u in results} == {'Alice', 'Bob'}

    def test_query_relationship(self, _db_cli):
        """测试关联模型查询"""
        results = _db_cli.query(Article, filters={
            'user_id__eq': 1,
            'status__eq': 'published'
        })
        assert len(results) == 1
        assert results[0].title == 'Python Guide'

    def test_query_with_existing_query(self, _db_cli):
        """测试传入已有query对象"""
        with _db_cli.session() as sess:
            base_query = sess.query(User).filter(User.is_active == 1)
            results = _db_cli.query(
                User, query=base_query, filters={'name__like': 'A%'})
            assert len(results) == 1
            assert results[0].name == 'Alice'

    def test_query_empty_filter(self, _db_cli):
        """测试空过滤条件"""
        results = _db_cli.query(User, filters={})
        assert len(results) == 3  # 应该返回所有用户

    def test_query_isnull_condition(self, _db_cli):
        """测试空值判断"""
        # 添加一个字段为空的用户
        with _db_cli.session() as session:
            session.add(User(id=4, name='David', age=28, is_active=None))
            session.commit()

        results = _db_cli.query(User, filters={
            'is_active__isnull': True
        })
        assert any(u.name == 'David' for u in results)

    def test_query_complex_condition(self, _db_cli):
        """测试复杂组合条件"""
        results = _db_cli.query(User, filters={
            'and': [
                {'or': [
                    {'age__ge': 30},
                    {'name__like': 'A%'}
                ]},
                {'not': {'is_active': 0}}
            ]
        })
        names = {u.name for u in results}
        assert 'Alice' in names
        assert 'Bob' not in names
        assert 'Charlie' in names

    def test_query_invalid_field(self, _db_cli, caplog):
        """测试无效字段"""
        # with pytest.raises(AttributeError):
        result = _db_cli.query(User, filters={'invalid_field__eq': 'value'})
        assert "invalid_field" in caplog.text

    def test_query_error_handling(self, _db_cli, caplog):
        """测试错误处理"""
        # 模拟错误条件
        results = _db_cli.query(User, filters={'name__invalid_op': 'value'})
        assert not results
        assert "query failed" in caplog.text


def test_not_operator_with_field(_db_cli):
    """测试字段级NOT操作符"""
    # filters = {
    #     'name__not': {'eq': 'Alice'},
    # }
    filters = {
        'and': [
            {'name__not': {'eq': 'Alice'}},
            {'status__not': {'eq': 'active'}},
        ]
    }
    condition = dict_to_sa_filter(User, filter_dict=filters)
    result = _db_cli.session().query(User).filter(condition).all()
    assert len(result) >= 1
    assert 'Alice' not in [u.name for u in result]


def test_in_operator(_db_cli):
    """测试IN操作符"""
    condition = dict_to_sa_filter(User, {
        'name__in': ['Alice', 'Bob']
    })
    result = _db_cli.session().query(User).filter(condition).all()
    assert len(result) == 2
    assert {u.name for u in result} == {'Alice', 'Bob'}


class TestModelConverterMixin:

    def test_to_dict(self, _db_cli):
        session = _db_cli.session()
        user = User(name='John Doe', age=30, email='john@example.com',
                    is_active=True, status='active')
        session.add(user)
        session.commit()

        user_dict = user.to_dict()
        assert isinstance(user_dict, dict)
        assert user_dict['name'] == 'John Doe'
        assert user_dict['age'] == 30
        assert user_dict['email'] == 'john@example.com'
        assert user_dict['is_active']
        assert user_dict['status'] == 'active'
        assert isinstance(user_dict['created_at'], str)
        assert isinstance(user_dict['updated_at'], str)

    def test_from_dict(self, _db_cli):
        session = _db_cli.session()
        user_dict = {
            'name': 'Jane Smith',
            'age': 25,
            'email': 'jane@example.com',
            'is_active': False,
            'status': 'inactive',
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        user = User.from_dict(user_dict)
        session.add(user)
        session.commit()

        retrieved_user = session.query(
            User).filter_by(name='Jane Smith').first()
        assert retrieved_user is not None
        assert retrieved_user.name == 'Jane Smith'
        assert retrieved_user.age == 25
        assert retrieved_user.email == 'jane@example.com'
        assert not retrieved_user.is_active
        assert retrieved_user.status == 'inactive'

    def test_to_dict_with_relationship(self, _db_cli):
        session = _db_cli.session()
        user = User(name='Bob Johnson', age=35,
                    email='bob@example.com', is_active=True, status='active')
        category = Category(name='Technology', creator=user)
        article = Article(title='New Tech Trends',
                          content='Some content', author=user, category=category)
        session.add_all([user, category, article])
        session.commit()

        user_dict = user.to_dict()
        assert isinstance(user_dict, dict)
        assert 'categories' in user_dict
        assert isinstance(user_dict['categories'], list)
        assert len(user_dict['categories']) == 1
        assert 'articles' in user_dict
        assert isinstance(user_dict['articles'], list)
        assert len(user_dict['articles']) == 1

    def test_from_dict_with_relationship(self, _db_cli):
        session = _db_cli.session()
        user_dict = {
            'name': 'Eve Brown',
            'age': 28,
            'email': 'eve@example.com',
            'is_active': True,
            'status': 'active',
            'categories': [
                {
                    'name': 'Science',
                    'articles': [
                        {
                            'title': 'Science Discoveries',
                            'content': 'Some science content'
                        }
                    ]
                }
            ]
        }

        user = User.from_dict(user_dict)
        session.add(user)
        session.commit()

        retrieved_user = session.query(
            User).filter_by(name='Eve Brown').first()
        assert retrieved_user is not None
        assert retrieved_user.name == 'Eve Brown'
        assert len(retrieved_user.categories) == 1
        category = retrieved_user.categories[0]
        assert category.name == 'Science'
        assert len(category.articles) == 1
        article = category.articles[0]
        assert article.title == 'Science Discoveries'
        assert article.content == 'Some science content'


class TestORMComparisonMixin:
    @pytest.fixture
    def user1(self):
        return User(
            id=1,
            created_at=datetime(2000, 1, 1, 0, 0, 0),
            updated_at=datetime(2000, 1, 1, 0, 0, 0),
            name='Alice',
            age=25,
            email='alice@example.com',
            is_active=True,
            status='active')

    @pytest.fixture
    def user2(self):
        return User(
            id=1,
            created_at=datetime(2000, 1, 1, 0, 0, 0),
            updated_at=datetime(2000, 1, 1, 0, 0, 0),
            name='Alice',
            age=25,
            email='alice@example.com',
            is_active=True,
            status='active')

    @pytest.fixture
    def user3(self):
        return User(
            id=3,
            created_at=datetime(2000, 1, 1, 0, 0, 0),
            updated_at=datetime(2000, 1, 1, 0, 0, 0),
            name='Bob',
            age=25,
            email='bob@example.com',
            is_active=True,
            status='active')

    def test_compare_without_filters(self, user1, user2):
        assert user1.compare(user2)

    def test_compare_not_equal_without_filters(self, user1, user3):
        assert not user1.compare(user3)

    def test_compare_with_include_keys(self, user1, user2):
        assert user1.compare(user2, include_keys=['name'])

    def test_compare_with_exclude_keys(self, user1, user3):
        assert user1.compare(user3,
                             exclude_keys=['id', 'name', 'email'])

    def test_compare_with_include_keys_and_exclude_keys(self, user1, user3):
        assert user1.compare(user3,
                             include_keys=['age'],
                             exclude_keys=['name', 'email'])
