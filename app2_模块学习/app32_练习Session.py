# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM

from flask import Flask,render_template,request,redirect,session,url_for
from flask_wtf import FlaskForm
import wtforms
from datetime import timedelta

app=Flask(__name__)
app.secret_key="1234"

class LoginForm(FlaskForm):
    username = wtforms.StringField('用户名：')
    password = wtforms.PasswordField('密码：')

@app.route("/",methods=["POST","GET"])
def login():
    session.clear()
    ins_LoginForm =LoginForm(request.form)
    if request.method=="POST":
        username =ins_LoginForm.username.data  # 通过类的实例化来获取表单中的username值
        password= ins_LoginForm.password.data
        if username=="1"and password=="1":
            session["admin"] =username
            return render_template("app32/public.html")
        if username=="2"and password=="2":
            session["normal_user"] =username
            return render_template("app32/public.html")
    session.permanent = True
    app.permanent_session_lifetime= timedelta(minutes=1)
    session.clear()
    return render_template("app32/login.html", form=ins_LoginForm)

@app.route("/public/")
def public():
    if session=={}:
        ins_LoginForm =LoginForm(request.form)
        return redirect(url_for("login"))
    if session.get("admin",None) is not None:
        return render_template("app32/AdminUser.html")
    else:
        return render_template("app32/public.html")

@app.route("/AdminUser/")
def AdminUser():
    if session=={}:
        return redirect(url_for("app32/login"))
    else:
        return render_template("app32/AdminUser.html")

if __name__ == '__main__':
    app.debug = True
    app.run(port=8081)


# login() 视图函数
# 1. 如果是管理员登录，则为session设置一个admin键，值为当前用户名，即admin
# 2. login函数，如果是普通用户登录，则为session设置一个normal_user键，值为当前用户名，即xiaoming
# 3. 在return render_template中，并没有把session传递给login页面，因为前面说了，session是全局的，随时随地都可以直接引用，无需传递
# 4. 设置了session的有效时间为一分钟，不作操作超过一分钟，则跳转至登录页面
# 5. 在该函数里清空了session，即只要一登陆，就先清空session，防止普通用户和管理员在同一台机器上使用同一个浏览器后，普通用户获取到管理员的session

# public() 视图函数
# 1. 当进入函数时，先判断，如果session为空，说明该登录者不是系统里的用户，他是通过猜地址进来的，那么就直接让他的页面跳转至登录页面
# 2. 如果session里的admin键的值不为空，则证明该用户是管理员，那么可点击管理员的可见链接跳转至AdminUser.html页面
# 3. 否则，则证明该用户为普通用户，那么可点击普通用户的可见链接跳转至public.html页面，即当前页面

# AdminUser() 视图函数
# 1. 当进入函数时，先判断，如果session为空，说明该登录者不是系统里的用户，他是通过猜地址进来的，那么就直接让他的页面跳转至登录页面，否则，证明该用户为管理员。
#
# 注意：
# 在这里，只要session不为空，就可判断其为管理员，因为在public()函数所对应的public.html模板中，已经设置了如果是管理员，则可见管理员链接，如果是普通用户，则不可见管理员链接，所有，只要能点击管理员链接进入管理员页面的，就一定是管理员。
# 综上所述，我们就无需再判断是否是管理员还是普通用户，只需判断其是否是通过猜测地址进入管理员页面的即可。