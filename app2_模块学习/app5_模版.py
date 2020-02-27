# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/2/26 4:15 下午

from flask import Flask

app = Flask(__name__) # 创建了一个Flask类的实例__name__是自定义的名称，也可以用其他的，如__main__等
@app.route("/index/") # 用route()装饰器来自定义自己的URL
def my_first(): # 创建一个函数，返回一个值
    user = {'username':'flask'} # 定义一个字典
    html = '''<!这是一个字符串，内容是一个html页面>
    <html>
    <head>
    <title>Home Page -Microblog</title>
    </head>
    <body>
    <h1>Hello, ''' +user['username'] + '''!</h1><!把字典里的值和heml字符串拼接起来（这是html注释的写法）>
    </body>
    </html>

    '''
    return html

if __name__ == '__main__':
    app.debug = True
    app.run() # 让这个这个应用跑起来


# 写一个简单的html页面