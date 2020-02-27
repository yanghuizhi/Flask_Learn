# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/2/26 4:15 下午

from flask import Flask,url_for

# 创建了一个Flask类的实例__name__是自定义的名称，也可以用其他的，如__main__等
app = Flask(__name__)

@app.route("/user/") # 用route()装饰器来自定义自己的URL
def user(): # 创建一个函数，返回一个值
    return"hello user"

@app.route("/reverse_url/") # 用route()装饰器来自定义自己的URL
def reverse_url():# 创建一个函数，返回一个值
    return"reverse url:"+url_for('user')

if __name__ == '__main__':
    app.debug = True
    app.run()

# 实际应用场景：把页面跳转至某URL
# 127.0.0.1:8000/reverse_url/
# 结果展示：reverse url:/user/