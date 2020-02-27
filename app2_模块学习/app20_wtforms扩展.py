# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM


from flask import Flask,render_template,flash,request,redirect
# from flask_wtf import Form  # 存在警告信息
from flask_wtf import FlaskForm
import wtforms

app = Flask(__name__) # 创建了一个Flask类的实例
app.secret_key="123"

# class loginform(Form): # 创建一个用于获取html页面数据的类，它必须继承自wtforms类的Form子类
class loginform(FlaskForm):  # 解决警告信息
    username=wtforms.StringField('用户名：',) # 设置username，html页面将从这里取数据
    password=wtforms.PasswordField('密 码：')# 设置password，html页面将从这里取数据
    for1=wtforms.StringField('username',default="我自己")
    for2=wtforms.RadioField("性别",choices=[(1,"男"),(2,"女")])
    for3=wtforms.SelectField("部  门：",choices=[(1,"开发部"),(2,"测试部"),(3,"配置管理部")])

@app.route("/",methods=["POST","GET"]) # 用route()装饰器来自定义自己的URL
def login():
    myform=loginform(request.form)  # 创建loginform类的实例化
    if request.method=="POST":
        username=myform.username.data # 通过类的实例化来获取表单中的username值
        password=myform.password.data # 通过类的实例化来获取表单中的password值
        if username=="1" and password=="1":
            return redirect("https://www.baidu.com")
        else:
            ErrorMessage="用户名或密码错误"
            return render_template("login20.html",ErrorMessage=ErrorMessage,form=myform)
    return render_template("login20.html",form=myform)

if __name__ == '__main__':
    app.debug = True
    app.run()

# 1. nder_template()返回页面时要把获取数据类的实例myform传入html页面，而form是固定写法，代表对应页面即login.html的表单，form=myform就是把myform传入login.html的form即表单
#
# 2. 不必考虑一个页面多个表单的情况，因为一个页面只会有一个表单
#
# 3. app.secret_key="123"是防止其他人恶意访问cookie从而获取到用户的session，该部分详见session处理章节