# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM


from flask import Blueprint

bp = Blueprint('errors', __name__)

from app.errors import handlers  # 底部导入避免循环依赖


# 错误处理Blueprint

# app/
#     errors/                    <-- blueprint package
#         __init__.py            <-- blueprint creation
#         handlers.py            <-- error handlers
#     templates/
#         errors/                <-- error templates
#             404.html
#             500.html
#     __init__.py                <-- blueprint registration