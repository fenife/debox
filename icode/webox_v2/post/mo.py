import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base

# 1.x 版本的基类定义方式
Base = declarative_base()

class ModelBase(Base):
    __abstract__ = True

    def to_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}

class Post(ModelBase):
    __tablename__ = "post"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, comment="id")
    user_id = sa.Column(sa.Integer, sa.ForeignKey("user.id"), nullable=False, comment="发布用户ID")
    cate_id = sa.Column(sa.Integer, sa.ForeignKey("cate.id"), nullable=True, comment="分类ID")
    title = sa.Column(sa.String(255), nullable=False, comment="文章中文标题")
    title_en = sa.Column(sa.String(255), nullable=True, default="", comment="文章英文标题")
    content = sa.Column(sa.Text, nullable=True, default="", comment="文章正文内容")

    # 1.x 简化写法：用 backref 一键生成反向关联，更简洁
    user = None
    cate = None

class User(ModelBase):
    __tablename__ = "user"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(255), nullable=False, comment="username")
    nickname = sa.Column(sa.String(255), nullable=False, comment="nickname")

    posts = []

class Category(ModelBase):
    __tablename__ = "category"
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String(255), nullable=False, comment="category name")

    posts = []

# 建表+会话
# engine = sa.create_engine("sqlite:///./blog.db", echo=True)
# Base.metadata.create_all(engine)
