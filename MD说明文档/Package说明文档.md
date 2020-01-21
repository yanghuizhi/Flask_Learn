# Welcome to Flask_Learn!

## flask 

- `render_template()` 函数: 调用Flask框架原生依赖的`Jinja2`模板引擎, 传入参数中的相应值替换{{...}}块. 

- `redirect()`: 这个函数指引浏览器自动重定向到它的参数所关联的URL. 

- `flash()`: 闪现消息，且只显示一次，将函数内的信息返回给`get_flashed_messages()`

- `url_for()`: 更好地管理链接,它使用URL到视图函数的内部映射关系来生成URL。


## python-dotenv 
Reads the key,value pair from .env and adds them to environment variable. 

- 手动设置的环境变量 > .env中设置的环境变量 > .flaskenv设置的环境变量
- .env存储敏感信息的环境变量
- .flaskenv存储公开环境变量

## Flask-WTF
用来处理`web`表单，集成WTForms，并带有 csrf 令牌的安全表单和全局的 csrf 保护的功能。

常用操作`from flask_wtf import FlaskForm` 导入基类

每次我们在建立表单所创建的类都是继承与flask_wtf中的FlaskForm，而FlaskForm是继承WTForms中forms。

```python
  form.hidden_tag()  # 自定义表单一定要加上，否则会提交不成功。这一行代码实质上是添加了一个隐藏字段csrf_token,这是一个随机生成的token，用来防范黑客攻击。
  form.validate_on_submit()  # 实例方法会执行form校验的工作, 全部通过之后就会返回True
  
  
```
  
## flask-sqlalchemy `or` flask_migrate
`flask-sqlalchemy` 是数据库软件的[ORM](https://baike.baidu.com/item/%E5%AF%B9%E8%B1%A1%E5%85%B3%E7%B3%BB%E6%98%A0%E5%B0%84/311152?fromtitle=ORM&fromid=3583252&fr=aladdin)，而是支持包含MySQL、PostgreSQL和SQLite在内的很多数据库软件。<br/>
`flask_migrate` 数据库迁移引擎.
  
    `db.Model`: 它是Flask-SQLAlchemy中所有模型的基类,字段被创建为`db.Column`类的实例  

```python
flask db init                # 创建迁移数据库，产生migrations的新目录
flask db migrate -m "..."    # 创建数据库迁移
flask db upgrade             # 将更改应用到数据库
flask db downgrade           # 回滚数据库迁移
```

## flask-login   
该插件管理用户登录状态，以便用户可以登录到应用，然后用户在导航到该应用的其他页面时，应用会“记得”该用户已经登录。

它还提供了“记住我”的功能，允许用户在关闭浏览器窗口后再次访问应用时保持登录状态。
## 
  
[BootStrap Popover](https://getbootstrap.com) 组件简介


