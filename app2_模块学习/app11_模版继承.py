# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM

from flask import Flask
from flask import render_template,request


# 创建了一个Flask类的实例__name__是自定义的名称，也可以用其他的，如__main__等
app = Flask(__name__)


@app.route("/one/") # 用route()装饰器来自定义自己的URL
def one(): # 创建一个函数，返回一个值
    return render_template("app11/index1.html")

@app.route("/two/") # 用route()装饰器来自定义自己的URL
def two(): # 创建一个函数，返回一个值
    return render_template("app11/index2.html")

if __name__ == '__main__':
    app.debug = True
    app.run()