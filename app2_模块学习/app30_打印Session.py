# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM


# coding=utf-8
from flask import Flask,render_template,request,redirect,session
from flask_wtf import FlaskForm
import wtforms

app=Flask(__name__)
app.secret_key="1234"

class LoginForm(FlaskForm):
    username = wtforms.StringField('用户名：')
    password = wtforms.PasswordField('密码：')

@app.route("/",methods=["POST","GET"])
def login():
    ins_LoginForm =LoginForm(request.form)
    print("session=",session)
    print("session=",session['csrf_token'])
    if request.method=="POST":
        username =ins_LoginForm.username.data  # 通过类的实例化来获取表单中的username值
        password= ins_LoginForm.password.data
        if username=="1"and password=="1":
            return render_template("index_13.html")
    return render_template("login20.html", form=ins_LoginForm)

if __name__ == '__main__':
    app.debug = True
    app.run()

# session= <SecureCookieSession {'csrf_token': '6ac702c14f6baf24dacd9785abf0b01d88cde287'}>
# session= 6ac702c14f6baf24dacd9785abf0b01d88cde287