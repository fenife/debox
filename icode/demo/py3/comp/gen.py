import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.mysql import pymysql

Base = declarative_base()


class User(Base):
    """用户表模型"""
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(50), nullable=False)
    age = sa.Column(sa.Integer)
    created = sa.Column(sa.DateTime, default=sa.func.now())


def gen_insert_sql(model, data):
    """
    生成可直接执行的带完整参数的 MySQL INSERT SQL 语句
    :param model: SQLAlchemy 模型类
    :param data: 要插入的数据，字典形式
    :return: 可直接执行的 SQL 语句
    """
    try:
        table = model.__table__
        insert_stmt = table.insert().values(**data)
        # 编译时替换为 MySQL 的 CURRENT_TIMESTAMP
        compiled = insert_stmt.compile(
            dialect=pymysql.dialect(),
            compile_kwargs={"literal_binds": True}
        )
        sql = str(compiled)
        sql = sql.replace("now()", "CURRENT_TIMESTAMP")
        sql += ";"
        return sql
    except Exception as e:
        print(e)
        return None


def gen_update_sql(model, data, condition):
    """
    生成可直接执行的带完整参数的 MySQL UPDATE SQL 语句
    :param model: SQLAlchemy 模型类
    :param data: 要更新的数据，字典形式
    :param condition: 更新的条件，如 {'id': 1}
    :return: 可直接执行的 SQL 语句
    """
    table = model.__table__
    update_stmt = table.update().values(**data)
    for key, value in condition.items():
        update_stmt = update_stmt.where(table.c[key] == value)
    compiled = update_stmt.compile(
        dialect=pymysql.dialect(),
        compile_kwargs={"literal_binds": True}
    )
    return str(compiled)


def gen_delete_sql(model, condition):
    """
    生成可直接执行的带完整参数的 MySQL DELETE SQL 语句
    :param model: SQLAlchemy 模型类
    :param condition: 删除的条件，如 {'id': 1}
    :return: 可直接执行的 SQL 语句
    """
    table = model.__table__
    delete_stmt = table.delete()
    for key, value in condition.items():
        delete_stmt = delete_stmt.where(table.c[key] == value)
    compiled = delete_stmt.compile(
        dialect=pymysql.dialect(), compile_kwargs={"literal_binds": True})
    return str(compiled)


def test_sql():
    user_data = {
        "name": "Alice",
        "age": 30
    }
    # 示例使用：插入多条数据
    sql = gen_insert_sql(User, user_data)
    print(sql)

    condition = {'id': 1}
    sql = gen_update_sql(User, user_data, condition)
    print(sql)

    sql = gen_delete_sql(User, condition)
    print(sql)


def _run_sql(sql_list):
    # 假设已经有数据库连接对象 conn
    from sqlalchemy import create_engine

    # 创建数据库引擎
    engine = create_engine(
        'mysql+pymysql://username:password@host:port/database_name')
    conn = engine.connect()
    try:
        for sql in sql_list:
            print("run sql: {}".format(sql))
            conn.execute(sql)
    except Exception as e:
        print(f"插入数据时出错: {e}")
    finally:
        conn.close()


def main():
    test_sql()


if __name__ == "__main__":
    main()
