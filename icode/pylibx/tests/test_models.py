from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    age = Column(Integer)
    is_active = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.now)
    status = Column(String(20))
    
    # 一对多关系：User -> Article
    articles = relationship("Article", back_populates="author")
    # 一对多关系：User -> Category (创建者)
    categories = relationship("Category", back_populates="creator")

class Article(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    content = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))
    category_id = Column(Integer, ForeignKey('categories.id'))
    status = Column(String(20))
    
    # 多对一关系：Article -> User
    author = relationship("User", back_populates="articles")
    # 多对一关系：Article -> Category
    category = relationship("Category", back_populates="articles")

class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey('users.id'))
    
    # 一对多关系：Category -> Article
    articles = relationship("Article", back_populates="category")
    # 多对一关系：Category -> User (创建者)
    creator = relationship("User", back_populates="categories")

