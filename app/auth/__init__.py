# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM


from flask import Blueprint

bp = Blueprint('auth', __name__)

from app.auth import routes


# 用户认证Blueprint
#
# app/
#     auth/                               <-- blueprint package
#         __init__.py                     <-- blueprint creation
#         email.py                        <-- authentication emails
#         forms.py       表单类            <-- authentication forms
#         routes.py      路由类            <-- authentication routes
#     templates/         模版类
#         auth/                           <-- blueprint templates
#             login.html
#             register.html
#             reset_password_request.html
#             reset_password.html
#     __init__.py                         <-- blueprint registration