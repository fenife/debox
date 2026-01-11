
from post.mo import User, Category, Post

user1 = User(id=1, name="admin", nickname="系统管理员")
user2 = User(id=2, name="test", nickname="测试员")
user3 = User(id=3, name="zhangsan", nickname="张三")
user4 = User(id=4, name="lisi", nickname="李四")
user5 = User(id=5, name="wangwu", nickname="王五")

cate1 = Category(id=1, name="Python编程")
cate2 = Category(id=2, name="SQLAlchemy教程")
cate3 = Category(id=3, name="后端开发")


post1 = Post(id=1, user_id=1, cate_id=1, user=user1, cate=cate1,
             title="Python基础",
             title_en="Python Basic Syntax Tutorial",
             content="Python是一种解释型、动态数据类型的高级程序设计语言")
post2 = Post(id=2, user_id=1, cate_id=2, user=user1, cate=cate2,
             title="SQLAlchemy模型定义",
             title_en="SQLAlchemy2.0 Model Best Practice",
             content="使用SQLAlchemy2.0的DeclarativeBase定义模型")
post3 = Post(id=3, user_id=2, cate_id=1, user=user2, cate=cate1,
             title="Python列表推导",
             title_en="Python List Comprehension & Generator",
             content="列表推导式可以快速生成列表")
post4 = Post(id=4, user_id=2, cate_id=3, user=user2, cate=cate3,
             title="FastAPI",
             title_en="FastAPI Build Light Backend",
             content="FastAPI是一款高性能的异步Python框架，开发效率极高。")
post5 = Post(id=5, user_id=3, cate_id=2, user=user3, cate=cate2,
             title="SQLAlchemy ORM",
             title_en="SQLAlchemy ORM Join Query",
             content="通过relationship定义关联关系后，可通过对象属性获取关联数据")
post6 = Post(id=6, user_id=3, cate_id=3, user=user3, cate=cate3,
             title="MySQL索引",
             title_en="MySQL Index Optimization",
             content="合理创建索引可以大幅提升查询效率")
post7 = Post(id=7, user_id=4, cate_id=1, user=user4, cate=cate1,
             title="Python装饰器",
             title_en="Python Decorator Usage",
             content="装饰器可以在不修改原函数代码的情况下，为函数增加额外功能")
post8 = Post(id=8, user_id=1, cate_id=3, user=user1, cate=cate3,
             title="开发工具",
             title_en="Developer Tools Recommend",
             content="VSCode这些工具可以极大提升开发效率")
post9 = Post(id=9, user_id=5, cate_id=2, user=user5, cate=cate2,
             title="ORM优缺点",
             title_en="ORM vs Native SQL",
             content="ORM开发效率高、可读性强，项目中可以根据场景灵活选择。")


user_list = [user1, user2, user3, user4, user5]

cate_list = [cate1, cate2, cate3]

post_list = [post1, post2, post3, post4, post5, post6, post7, post8, post9]

for u in user_list:
    u.posts = [p for p in post_list if u.id == p.user_id]

for c in cate_list:
    c.posts = [p for p in post_list if c.id == p.cate_id]
