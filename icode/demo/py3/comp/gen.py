import sqlalchemy as sa
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.mysql import pymysql
from datetime import datetime

Base = declarative_base()


class User(Base):
    """用户表模型"""
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(50), nullable=False)
    age = sa.Column(sa.Integer)
    created = sa.Column(sa.DateTime, default=sa.func.now())


def gen_insert_sql1(model, data):
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


def gen_update_sql1(model, data, condition):
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


def gen_delete_sql1(model, condition):
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


def get_insert_sql(model, data):
    """生成合并后的 MySQL INSERT SQL 语句"""
    table = model.__table__
    columns = table.columns
    column_names = [col.name for col in columns]

    # 生成 VALUES 部分
    values = []
    for col in columns:
        value = data.get(col.name)
        if value is None:
            if col.default is not None:
                value = col.default.arg  # 使用默认值
            else:
                value = "NULL"  # 数据库 NULL

        # 根据列类型处理数据格式
        if isinstance(col.type, sa.String):
            # 转义单引号并包裹单引号
            escaped = str(value).replace("'", "''")
            values.append(f"'{escaped}'")
        elif isinstance(col.type, sa.Integer):
            values.append(str(value))
        else:
            # 其他类型默认按字符串处理
            escaped = str(value).replace("'", "''")
            values.append(f"'{escaped}'")

    # 拼接完整 SQL
    columns_str = ', '.join(column_names)
    value_str = ', '.join(values)
    sql = f"INSERT INTO {table.name} ({columns_str}) VALUES ({value_str});"
    return sql

def get_update_sql(model, data, where_condition={}):
    """生成 MySQL UPDATE SQL 语句
    
    Args:
        model: SQLAlchemy 模型类
        data: 要更新的字段字典 {字段名: 值}
        where_condition: 更新条件，可以是字典或字符串
                        字典格式：{字段名: 值}
                        字符串格式：直接作为 WHERE 条件
    """
    table = model.__table__
    
    # 处理 SET 部分
    set_parts = []
    for col in table.columns:
        if col.name in data:
            value = data[col.name]
            
            # 根据列类型处理值
            if value is None:
                set_parts.append(f"{col.name} = NULL")
            elif isinstance(col.type, sa.String):
                escaped = str(value).replace("'", "''")
                set_parts.append(f"{col.name} = '{escaped}'")
            elif isinstance(col.type, (sa.Integer, sa.Float)):
                set_parts.append(f"{col.name} = {value}")
            elif isinstance(col.type, sa.DateTime):
                if isinstance(value, datetime):
                    formatted = value.strftime("%Y-%m-%d %H:%M:%S")
                    set_parts.append(f"{col.name} = '{formatted}'")
                else:
                    set_parts.append(f"{col.name} = '{value}'")
            else:
                escaped = str(value).replace("'", "''")
                set_parts.append(f"{col.name} = '{escaped}'")
    
    # 处理 WHERE 条件
    if where_condition is None:
        raise ValueError("必须提供 where_condition 或数据中包含主键 id")
    
    if isinstance(where_condition, dict):
        where_parts = []
        for col_name, value in where_condition.items():
            col = table.columns[col_name]
            
            if value is None:
                where_parts.append(f"{col_name} IS NULL")
            elif isinstance(col.type, sa.String):
                escaped = str(value).replace("'", "''")
                where_parts.append(f"{col_name} = '{escaped}'")
            elif isinstance(col.type, (sa.Integer, sa.Float)):
                where_parts.append(f"{col_name} = {value}")
            elif isinstance(col.type, sa.DateTime):
                if isinstance(value, datetime):
                    formatted = value.strftime("%Y-%m-%d %H:%M:%S")
                    where_parts.append(f"{col_name} = '{formatted}'")
                else:
                    where_parts.append(f"{col_name} = '{value}'")
            else:
                escaped = str(value).replace("'", "''")
                where_parts.append(f"{col_name} = '{escaped}'")
        
        where_clause = " AND ".join(where_parts)
    else:
        where_clause = where_condition
    
    # 构建完整 SQL
    set_clause = ", ".join(set_parts)
    sql = f"UPDATE {table.name} SET {set_clause} WHERE {where_clause};"
    return sql


def get_delete_sql(model, condition):
    """生成 MySQL DELETE SQL 语句
    
    Args:
        model: SQLAlchemy 模型类
        condition: 删除条件字典 {字段名: 值}
    """
    table = model.__table__
    
    # 处理 WHERE 条件
    where_parts = []
    for col_name, value in condition.items():
        col = table.columns[col_name]
        
        if value is None:
            where_parts.append(f"{col_name} IS NULL")
        elif isinstance(col.type, sa.String):
            escaped = str(value).replace("'", "''")
            where_parts.append(f"{col_name} = '{escaped}'")
        elif isinstance(col.type, (sa.Integer, sa.Float)):
            where_parts.append(f"{col_name} = {value}")
        elif isinstance(col.type, sa.DateTime):
            if isinstance(value, datetime):
                formatted = value.strftime("%Y-%m-%d %H:%M:%S")
                where_parts.append(f"{col_name} = '{formatted}'")
            else:
                where_parts.append(f"{col_name} = '{value}'")
        else:
            escaped = str(value).replace("'", "''")
            where_parts.append(f"{col_name} = '{escaped}'")
    
    where_clause = " AND ".join(where_parts)
    return f"DELETE FROM {table.name} WHERE {where_clause};"


def test_sql():
    user_data = {
      "name": "Alice",
       "age": 30
    }
        # 示例使用：插入多条数据
    sql = get_insert_sql(User, user_data)
    print(sql)

    condition = {'id': 1}
    sql = get_update_sql(User, user_data, condition)
    print(sql)

    sql = get_delete_sql(User, condition)
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
