# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/2/26 4:15 下午

from flask import Flask   # 导入Flask类，这个类的实例化就是wsgi的应用

# 创建了一个Flask类的实例, 创建Flask实例的过程中，可以执行静态代码默认目录
# __name__是自定义的名称，也可以用其他的，如__main__等
app = Flask(__name__)

@app.route("/user/") # 用route()装饰器来自定义自己的URL
def test(): # 创建一个函数，返回一个值
    return"hello user"

if __name__ == '__main__':
    app.debug = True  # 打开debug调试功能
    app.run()  # 应用的启动命令
    # app.run(port=9000, host="0.0.0.0")  # 可修改主机和端口
    # app.run(debug=True)       # debug 开启方式二
