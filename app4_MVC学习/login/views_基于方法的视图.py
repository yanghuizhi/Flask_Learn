# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/2/27 7:50 下午

from flask.views import MethodView
from flask import render_template,request

class login(MethodView):
    def get(self):
        return render_template("/login.html/")
    def post(self):
        pass

class zhuce(MethodView):
    def get(self):
        return render_template("/zhuce.html/")
    def post(self):
        pass

# 1. 同样是每个类对应一个页面，且类名与页面名要一致
# 2. 每个类都要继承自flask.views.MethodView
# 3. 类里只有两个方法，get和post，分别对应了get请求和post请求