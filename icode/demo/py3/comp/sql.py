
############################################################
# 插入
from sqlalchemy.orm import Session, declarative_base
from sqlalchemy.dialects import mysql
import sqlalchemy as sa

# 创建 declarative base 类
Base = declarative_base()

class User(Base):
    """用户表模型"""
    __tablename__ = "users"  # 数据库表名

    # 定义字段（主键自动生成）
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(50), nullable=False)  # 字符串类型，长度限制50，非空
    age = sa.Column(sa.Integer)
    city = sa.Column(sa.String(100), default="Unknown")  # 默认值


def compile_stmt_sql(stmt):
    stmt_sql = stmt.compile(
        dialect=mysql.dialect(),
        compile_kwargs={"literal_binds": True}  # 直接绑定参数
    )
    return str(stmt_sql)


# 创建一个待插入的对象
user = User(name="Bob", age=25)

# 手动生成 INSERT 语句
stmt = Session().add(user)  # 添加对象到会话
insert_stmt = Session().flush([user])  # 触发 SQL 生成

# 获取编译后的 SQL（需结合模型元数据）
insert_sql = sa.insert(User.__table__).values(name="Bob", age=25)
# insert_sql = insert_sql.compile(
#     dialect=mysql.dialect(),
#     compile_kwargs={"literal_binds": True}  # 直接绑定参数
# )
# print(insert_sql)
print(compile_stmt_sql(insert_sql))


############################################################
# 更新
# 手动生成 UPDATE 语句
stmt = (
    sa.update(User)
    .where(User.name == "Alice")
    .values(age=30)
    .compile(
        dialect=mysql.dialect(),
        compile_kwargs={"literal_binds": True}
    )
)
print(stmt)

############################################################

# 手动生成 DELETE 语句
stmt = (
    sa.delete(User)
    .where(User.id == 1)
    .compile(
        dialect=mysql.dialect(),
        compile_kwargs={"literal_binds": True}
    )
)
print(stmt)

