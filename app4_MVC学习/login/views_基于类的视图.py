# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/2/27 7:50 下午

from flask.views import View
from flask import render_template,request

class login(View):
    methods = ["GET","POST"]
    def dispatch_request(self):
        if request.method=="GET":
            pass
        else:
            pass
        return render_template("/login.html/")

class zhuce(View):
    methods = ["GET", "POST"]
    def dispatch_request(self):
        if request.method=="POST":
            pass
        else:
            pass
        return render_template("/zhuce.html/")


# 1.每一个页面对应一个类，类的名称要和页面名称一致，且必须继承自flask.views.View
# 2.可在类里面，函数外面，指定该类所对应的页面的数据发送方法，即GET或POST
# 注意：在指定数据发送方法时，methods是带s的，在判断数据发送方法时，request.method是不带s的
# 3. 类里的函数必须叫做dispatch_request(self)这是必须写死的