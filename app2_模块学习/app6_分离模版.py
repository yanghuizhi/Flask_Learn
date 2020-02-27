# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM

from flask import Flask
from flask import render_template,request

app = Flask(__name__)
# 创建了一个Flask类的实例__name__是自定义的名称，也可以用其他的，如__main__等

@app.route("/login",methods=["GET","POST"]) # 用route()装饰器来自定义自己的URL
@app.route('/',methods=["GET","POST"])
def login(): # 创建一个函数，返回一个值
    return render_template('index_6.html', thismethod=request.method)

if __name__ == '__main__':
    app.debug = True
    app.run() # 让这个这个应用跑起来

# 注意：
#
# 1. 页面里有一个form表单，定义了表单发送请求的方式是POST
#
# 2. 在视图函数里，通过request.method来获取表单提交时的方式，并把获取的结果赋给了thismethod变量
#
# 3. 在视图函数的装饰器里指定了接收和发送请求的方法是GET和POST
#
# 4. 视图函数通过render_template把thismethod传递给了login.html
#
# 5. 发送请求是指点击提交按钮的一瞬间所发送的请求所使用的方法，所以，当你在浏览器上点击提交按钮的时候，request.method方法就会捕捉到你使用的方法，然后在页面上显示出来是 post
#
# 6. 当进入页面时，显示的是GET方法，说明视图函数捕捉到的方法就是GET，既然已经指定了POST，为什么还是GET呢？因为进入页面这个操作默认就是GET方法，而我们指定的POST方法是指提交的一瞬间所使用的方法，不是进入页面的方法
#
# 7. 点击提交按钮后，页面会显示POST方法
#
# 那是因为我们在login.html页面的表单里定义了参数传递的方法是POST，所以在点击按钮后，页面就会以POST方式进行提交，被request.method捕捉后显示在页面上