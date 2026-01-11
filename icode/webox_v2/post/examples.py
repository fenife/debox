
from post.mo import User, Category, Post


user_list = [
    User(id=1, name="admin", nickname="系统管理员"),
    User(id=2, name="test", nickname="测试员"),
    User(id=3, name="zhangsan", nickname="张三"),
]

cate_list = [
    Category(id=11, user_id=1, name="Python编程"),
    Category(id=12, user_id=1, name="后端开发"),
    Category(id=21, user_id=2, name="SQL"),
    Category(id=22, user_id=2, name="工具"),
    Category(id=31, user_id=3, name="SQLAlchemy"),
]

post_list = [
    Post(id=111, user_id=1, cate_id=11,
         title="Python基础",
         title_en="Python Basic Syntax Tutorial",
         content="Python是一种解释型、动态数据类型的高级程序设计语言"),
    Post(id=112, user_id=1, cate_id=11,
         title="Python列表推导",
         title_en="Python List Comprehension & Generator",
         content="列表推导式可以快速生成列表"),
    Post(id=113, user_id=1, cate_id=11,
         title="Python装饰器",
         title_en="Python Decorator Usage",
         content="装饰器可以在不修改原函数代码的情况下，为函数增加额外功能"),
    Post(id=121, user_id=1, cate_id=12,
         title="FastAPI",
         title_en="FastAPI Build Light Backend",
         content="FastAPI是一款高性能的异步Python框架，开发效率极高。"),
    Post(id=211, user_id=2, cate_id=21,
         title="MySQL索引",
         title_en="MySQL Index Optimization",
         content="合理创建索引可以大幅提升查询效率"),
    Post(id=221, user_id=2, cate_id=22,
         title="开发工具",
         title_en="Developer Tools Recommend",
         content="VSCode这些工具可以极大提升开发效率"),
    Post(id=311, user_id=3, cate_id=31,
         title="SQLAlchemy模型定义",
         title_en="SQLAlchemy2.0 Model Best Practice",
         content="使用SQLAlchemy2.0的DeclarativeBase定义模型"),
    Post(id=312, user_id=3, cate_id=31,
         title="SQLAlchemy ORM",
         title_en="SQLAlchemy ORM Join Query",
         content="通过relationship定义关联关系后，可通过对象属性获取关联数据"),
    Post(id=313, user_id=3, cate_id=31,
         title="ORM优缺点",
         title_en="ORM vs Native SQL",
         content="ORM开发效率高、可读性强，项目中可以根据场景灵活选择。"),
]


def _get_user(uid):
    user = None
    for u in user_list:
        if u.id == uid:
            user = u
    return user


def _get_cate(cid):
    cate = None
    for c in cate_list:
        if c.id == cid:
            cate = c
    return cate


for u in user_list:
    u.cates = [c for c in cate_list if u.id == c.user_id]
    u.posts = [p for p in post_list if u.id == p.user_id]

for c in cate_list:
    c.user = _get_user(c.user_id)
    c.posts = [p for p in post_list if c.id == p.cate_id]

for p in post_list:
    p.user = _get_user(p.user_id)
    p.cate = _get_cate(p.cate_id)
