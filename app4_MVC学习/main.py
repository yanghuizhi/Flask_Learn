# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/2/27 7:50 下午


from flask import Flask
from login.views import *

app = Flask(__name__) # 创建了一个Flask类的实例
app.secret_key="123"

app.add_url_rule("/login/",view_func=login.as_view("login"))

app.add_url_rule("/zhuce/",view_func=zhuce.as_view("zhuce"))

if __name__ == '__main__':
    app.debug = True
    app.run(port=8080)

# 1. 主文件里只为视图函数设置URL规则
# 2. app.add_url_rule中的/login/和/zhuce/均代表各自的URL
# 3. view_func=login.as_view("login"))或view_func=login.as_view("zhuce"))中的login和zhuce代表的是视图函数里类的函数名，也叫中节点，相当于不使用MVC时视图函数的名称，由于在基于类的视图中，类里的视图函数的名称是统一的，没有自己独立的名称，所以要在主函数里指定一个其自己的名称，在页面中，如果需要跳转到该页面，href后面写的就是主函数里指定的函数名