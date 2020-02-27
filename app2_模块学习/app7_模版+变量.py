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


@app.route("/") # 用route()装饰器来自定义自己的URL
def user(): # 创建一个函数，返回一个值
    fuser=User("12345","YanghuiZhi")# 把User类实例化
    return render_template("index_7.html",user=fuser)# 把User类的实例化传入模板中


if __name__ == '__main__':
    app.debug = True
    app.run() # 让这个这个应用跑起来


# 1.	引入了变量文件的类
#
# 2.	实例化了变量文件的类
#
# 3.	把变量文件类的实例传入了模板