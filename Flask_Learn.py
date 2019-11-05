# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2019/10/29 2:15 PM

"""
    定义Flask应用程序实例的顶层,它仅拥有一个导入应用程序实例的行
"""


from app import app, db, cli
from app.models import User, Post



@app.shell_context_processor  # 添加一个shell上下文，方便咱们操作
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}