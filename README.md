# dm-sqlalchemy2.0 (达梦SQLAlchemy 错误修复版)

## 项目背景
由于达梦数据库官方提供的 `sqlalchemy2.0` 在实际应用中存在多种问题，且官方更新较慢，无法及时响应社区反馈。本项目旨在解决 `dm-sqlalchemy` 在 SQLAlchemy 2.0 适配中的错误和兼容性问题，为开发者提供更稳定的解决方案。

## 达梦sqlalchemy版本
- 2.0.1

## 安装方式
- 将sqlalchemy2.0 文件夹替换到 drivers\python\sqlalchemy2.0

## 已修复问题
1. **自增id返回异常(id值不对)问题**
- 代码位置 sqlalchemy_dm/base.py 1659行
- 复现案例
```python
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker

conn_url = 'dm+dmPython://SYSDBA:pwd@127.0.0.1:30236'
engine = create_engine(conn_url, echo=True, connect_args={'local_code': 1, 'connection_timeout': 15})
Session = sessionmaker(bind=engine)

class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    username = Column(String(64), nullable=False, unique=True)

with Session() as session:
    # 指定id=100
    user = User(id=100, username="test")
    session.add(user)
    session.commit()
    # 指定id打乱自增顺序后，新插入的不指定id时，返回的id异常
    user2 = User(username="test2")
    session.add(user2)
    session.flush()
    session.commit()
    # 此时显示 id=2, 实际数据库是101
    print(user2.id)
```

2. **插入datetime类型数据异常**
- 代码位置 sqlalchemy_dm/dmPython.py 443行
- 复现案例
```python
from datetime import datetime
with Session() as session:
    user = User(username="test", create_time=datetime.now())
    session.add(user)
    session.commit()
# 报错
    """
  File "/miniconda/lib/python3.11/site-packages/sqlalchemy_dm-2.0.1-py3.11.egg/sqlalchemy_dm/dmPython.py", line 446, in do_executemany
UnboundLocalError: cannot access local variable 'str_result' where it is not associated with a value
    """
```

3. **使用insert().values()批量插入异常**
- 代码位置 sqlalchemy_dm/base.py 926行
- 复现案例
```python
from sqlalchemy import insert
with Session() as session:
    session.execute(insert(User).values([{"username": "test1"}, {"username": "test2"}]))
# 报错 dmPython not supports_multivalues_insert
```

## 使用小贴士
### 字段名与关键字冲突问题
达梦列命名有一些关键字, 如 section, size, 使用sqlalchemy别名解决
```python
class Model(Base):
    section = Column("section_alias", Integer, nullable=False)
    # to_dict 使用 self.__mapper__.column_attrs 解决别名返回
    def to_dict(self):
        res = {}
        for c in self.__mapper__.column_attrs:
            res[c.key] = getattr(self, c.key, None)
```

### Json问题
- 使用 CLOB 作为json字段
```python
from sqlalchemy import Column, TypeDecorator, CLOB
class Json(TypeDecorator):
    impl = CLOB 
    cache_ok = True  

    def process_bind_param(self, value: (dict, list), dialect):
        if value is not None:
            value = json.dumps(value, ensure_ascii=False, cls=CustomJSONEncoder)
        return value

    def process_result_value(self, value: str, dialect):
        if value is not None:
            value = json.loads(value)
        return value

class Model(Base):
    config = Column(Json, nullable=False)
```

## 目标
希望达梦sqlalchemy 有一个github项目可以实时共享错误信息，修改发布最新版本
