# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM

from flask import Flask
from flask import render_template,flash,request


app = Flask(__name__) # 创建了一个Flask类的实例
app.secret_key="123"

@app.route("/") # 用route()装饰器来自定义自己的URL
def start():
    flash("欢迎登录")
    return render_template("index_13.html")

@app.route("/login/", methods=["POST"])  # 用route()装饰器来自定义自己的URL
def login(): # 创建一个函数，返回一个值
    form=request.form
    username=form.get("username")
    password=form.get("password")

    if not username:
        flash("用户名不能为空")
        return render_template("index_13.html")
    elif not password:
        flash("密码不能为空")
        return render_template("index_13.html")
    elif username=="1" and password=="1":
        flash("登录成功")
        return render_template("index_13.html")
    else:
        flash("用户名或密码错误")
        return render_template("index_13.html")

if __name__ == '__main__':
    app.debug = True
    app.run()

# 1. 模板文件中形式的动作必须要写成action =“ / login /”，注意后面必须有/，因为路由文件里的视图函数的装饰器里的URL就是带/的
#
# 2. 路由文件中的if语句一定要写成非用户名：，不能写成if username == None，这样写的话，这条if语句的值将永远为Falase，这是jinja的语法
#
# 3. 在路由文件中，首先用start（）函数来显示login.html，而login.html中的{{get_flashed_messages（）[0]}}使用显示提示信息，当刚刚登录页面时，该信息就是start（ ）函数里的flash（“欢迎登录”）
#
# 4. 当点击提交按钮时，提交触发了POST方法，而POST方法又触发了路由文件里的login（）函数，于是就开始运行函数内部的内容
#
# 5. 每一次单击了提交按钮后，由于登录（）函数被触发执行，模板文件里的{{get_flashed_messages（）[0]}}}对应登录（）下一个某个语句如果下一个flash（“提示内容“），并且每个每个里面的最后一句都是返回到login.html页面，即完成了点击提交按钮后的一些列动作，页面仍要显示login.html