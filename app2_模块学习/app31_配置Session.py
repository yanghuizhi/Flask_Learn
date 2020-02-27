# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM

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
    if request.method=="POST":
        username =ins_LoginForm.username.data  # 通过类的实例化来获取表单中的username值
        password= ins_LoginForm.password.data
        session["admin"] =username
        if username=="1"and password=="1":
            return render_template("Sess.html")
    return render_template("login15.html", form=ins_LoginForm)

@app.route("/tem/",methods=["POST","GET"])
def AdminUser():
    ins_LoginForm =LoginForm(request.form)
    if session["admin"] is not None:
        render_template("Sess.html")
    else:
        return render_template("login15.html", form=ins_LoginForm)

if __name__ == '__main__':
    app.debug = True
    app.run()

# 在视图函数login()中，通过session["admin"]=username这条语句来为当前用户设置session，设置的session的键为"admin"，值为其登录名
#
# 在视图函数AdminUser()中写到，如果session的admin键不为空，那么证明该人员为管理员