
## db util 
### DBClient query 函数的可选操作：
```text
字典键格式	SQL等价  示例
field	    =	    {"age": 25}
field__ne	!=	    {"status__ne": "deleted"}
field__gt	>	    {"score__gt": 90}
field__lt	<	    {"age__lt": 18}
field__ge	>=	    {"quantity__ge": 100}
field__le	<=	    {"price__le": 50.0}
field__like	LIKE	{"name__like": "John%"}
field__in	IN	    {"id__in": [1,2,3]}
or/and	    OR/AND	见示例

字典键格式	     SQL 等价	              示例
field__isnull	IS NULL / IS NOT NULL	{"email__isnull": True}
field__not	    反向操作符	             {"name__not": {"like": "%test%"}}
not	            NOT 逻辑	             {"not": {"age__gt": 18}}
```
### 示例
```python
# 自定义操作符处理器
OPERATOR_MAP = {
    'eq': lambda c, v: c == v,
    'neq': lambda c, v: c != v,
    'gt': lambda c, v: c > v,
    # 添加自定义操作符...
}

def register_operator(op_name: str, handler: Callable):
    OPERATOR_MAP[op_name] = handler

# 关联关系查询
# 使用关联查询 WHERE EXISTS (SELECT 1 FROM posts WHERE ...)
filter_dict = {
    "posts__any": {
        "title__like": "%Python%"
    }
}

# JSON字段查询
filter_dict = {
    "meta__json_key->>'$.address.city'": "New York"
}

# 空值处理
filter_dict = {
    "description__isnull": True
}

# 多层 NOT 嵌套处理
# 支持无限级嵌套
{
    "not": {
        "not": {
            "name": "John"
        }
    }
}
# WHERE NOT (NOT (name = 'John')) 
# 等价于 WHERE name = 'John'

# 自动操作符反转
# 当使用 field__not 语法时，系统会自动转换操作符：
# 原始条件
{"age__not": {"gt": 18}}
# 转换后
age <= 18

# 复合空值判断
{
    "or": [
        {"phone__isnull": True},
        {"phone": ""}
    ]
}
# WHERE phone IS NULL OR phone = ''
```

### 错误处理机制
```python
## 类型校验：
# 错误示例
{"email__isnull": "yes"}  # 非布尔值
# 抛出 ValueError: isnull 只接受布尔值 True/False

## 无效操作符：
{"age__invalid_op": 5}
# 抛出 ValueError: 不支持的运算符: invalid_op

## 字段不存在：
{"invalid_field__gt": 10}
# 抛出 AttributeError: 模型 <User> 没有字段 invalid_field
```

### 性能优化建议
```python
## 条件缓存：
from functools import lru_cache

@lru_cache(maxsize=128)
def get_column(model, field_name):
    return getattr(model, field_name, None)

## 预编译表达式：
compiled_filter = session.prepare_condition(condition)

## 批量处理：
def bulk_filter(models, filters_list):
    return [dict_to_sqlalchemy_filter(m, f) for m, f in zip(models, filters_list)]
```