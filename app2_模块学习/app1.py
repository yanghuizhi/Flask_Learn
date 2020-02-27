# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/2/26 4:15 下午

from flask import Flask

# 创建了一个Flask类的实例__name__是自定义的名称，也可以用其他的，如__main__等
app = Flask(__name__)

@app.route("/user/") # 用route()装饰器来自定义自己的URL
def test(): # 创建一个函数，返回一个值
    return"hello user"

if __name__ == '__main__':
    app.debug = True  # 打开debug调试功能
    app.run()
