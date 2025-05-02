from datetime import datetime
import sqlalchemy as sa
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class ModelBase(Base):
    __abstract__ = True

    id = sa.Column(sa.Integer, primary_key=True)
    created_at = sa.Column(sa.DateTime, default=datetime.now)
    updated_at = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

class User(ModelBase):
    __tablename__ = 'users'
    
    name = sa.Column(sa.String(50))
    age = sa.Column(sa.Integer)
    email = sa.Column(sa.String(100))
    is_active = sa.Column(sa.Boolean)
    status = sa.Column(sa.String(20))
    
    # 一对多关系：User -> Article
    articles = relationship("Article", back_populates="author")
    # 一对多关系：User -> Category (创建者)
    categories = relationship("Category", back_populates="creator")

class Article(ModelBase):
    __tablename__ = 'articles'
    
    title = sa.Column(sa.String(100))
    content = sa.Column(sa.String)
    user_id = sa.Column(sa.Integer, ForeignKey('users.id'))
    category_id = sa.Column(sa.Integer, ForeignKey('categories.id'))
    status = sa.Column(sa.String(20))
    
    # 多对一关系：Article -> User
    author = relationship("User", back_populates="articles")
    # 多对一关系：Article -> Category
    category = relationship("Category", back_populates="articles")

class Category(ModelBase):
    __tablename__ = 'categories'
    
    name = sa.Column(sa.String(50))
    user_id = sa.Column(sa.Integer, ForeignKey('users.id'))
    
    # 一对多关系：Category -> Article
    articles = relationship("Article", back_populates="category")
    # 多对一关系：Category -> User (创建者)
    creator = relationship("User", back_populates="categories")

