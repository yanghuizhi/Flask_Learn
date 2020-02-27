# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM

from flask import Flask,render_template,flash,request,redirect

app = Flask(__name__) # 创建了一个Flask类的实例

@app.route("/login/",methods=["POST","GET"]) # 用route()装饰器来自定义自己的URL
def start():
    if request.method=="POST":
        username=request.form.get("username")
        password=request.form.get("password")
        print("username",username)
        print("password",password)
        if username=="1" and password=="1":
            return redirect("https://www.baidu.com")
    else:
        ErrorMessage="用户名或密码错误"
        print("ErrorMessage= ", ErrorMessage)
        return render_template("login15.html",ErrorMessage=ErrorMessage)
    return render_template("login15.html")

if __name__ == '__main__':
    app.debug = True
    app.run(port=8080)

# 1. 由于render_template默认是GET方法，所以必须加上【if request.method=="POST":】这句，否则，由于你没有点击按钮，所以username和password不可能获取到值，这时他们俩都是None，那么就会走else语句块，这会导致一进入页面就会有那句消息提示。而加上了【if request.method=="POST":】，由于render_template默认是GET方法，所以进入页面后不会执行【if request.method=="POST":】语句块内的代码，页面上就不会有消息提示
#
# 2. 如果返回的页面不是templates文件夹下的页面，那么就不能使用render_template()方法，必须使用redirect()方法，且需要先行引入
#
# 3. app.run(port=8080)可以自定义端口，不使用默认的5000