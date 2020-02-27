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
    return render_template("index_10.html",user_list=thisuser_list) # 把User类的实例化传入模板中


if __name__ == '__main__':
    app.debug = True
    app.run() # 让这个这个应用跑起来

# *{{loop.变量}} 有序号循环*
# 使用{{loop.index}}来自动生成页面上的序号
#
# 注意：loop.index不是python的语法，而是jinja2的语法，用于在模板上生成一个显示用的序号
#
# 注意：
#
# 1.	这个序号只是显示用的，与数据库里的ID无关
#
# 2.	由于不是python的语法，而是用来显示在模板上给用户看的是，所以它从1开始，而不像python从0开始
#
# 3.	{{loop.index}}通常和table配合使用，因为只有table才能循环展示数据
