# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM

from flask import Flask
from flask import render_template,flash


app = Flask(__name__)  # 创建了一个Flask类的实例
app.secret_key="123"

@app.route("/MessageHint/") # 用route()装饰器来自定义自己的URL
def one(): # 创建一个函数，返回一个值
    flash("消息提示出来了")
    return render_template("index_12.html")

if __name__ == '__main__':
    app.debug = True
    app.run()