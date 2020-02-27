# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM

from flask import Flask
from flask import render_template,request


# 创建了一个Flask类的实例__name__是自定义的名称，也可以用其他的，如__main__等
app = Flask(__name__)

# 创建了一个类，里面定义了userid和username
class User():
    def __init__(self,userid,username):
        self.userid=userid
        self.username=username

# 用route()装饰器来自定义自己的URL
@app.route("/<user_id>")
def user(user_id): # 创建一个函数，返回一个值
    fuser=None
    if str.isdigit(user_id)== 1:
        fuser=User("007","智哥") # 把User类实例化
    return render_template("index_8.html",user=fuser) # 把User类的实例化传入模板中


if __name__ == '__main__':
    app.debug = True
    app.run() # 让这个这个应用跑起来

# 如果输入的URL变量是数字，则实例化User类为fuser，否则fuser就为空，最终把fuser传入模板