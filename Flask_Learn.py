# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/31 2:32 PM


from app import create_app, db, cli
from app.models import User, Post, Message, Notification, Task

app = create_app()  # 在顶级目录中调用应用工厂
cli.register(app)   # 注册cli


@app.shell_context_processor  # 此装饰器会将函数注册为 shell 上下文函数
def make_shell_context():
   # 运行 flask shell 时, 调用该函数并返回注册的项目, 函数返回一个字典格式.
    return {'db': db, 'User': User, 'Post': Post,
            'Message': Message, 'Notification': Notification, 'Task': Task}

print(make_shell_context.__dict__)