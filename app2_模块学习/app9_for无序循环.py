# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM

from flask import Flask
from flask import render_template,request


# 创建了一个Flask类的实例__name__是自定义的名称，也可以用其他的，如__main__等
app = Flask(__name__)

# 用route()装饰器来自定义自己的URL
@app.route("/")
def user(): # 创建一个函数，返回一个值
    thisuser_list = ["MichaelJackson" + str(i) for i in range(1, 11)]
    return render_template("index_9.html",user_list=thisuser_list) # 把User类的实例化传入模板中


if __name__ == '__main__':
    app.debug = True
    app.run() # 让这个这个应用跑起来

# *无序号循环*