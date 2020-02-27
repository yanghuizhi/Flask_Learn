# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/2/26 4:15 下午

from flask import Flask

app = Flask(__name__)

@app.route("/user/") # 自定义url
def index2(): # 创建一个函数，返回一个值
    return "hello word"

if __name__ == '__main__':
    app.debug = True  # 打开debug调试功能
    app.run(host='127.0.0.1', port=8000)

# 由于route装饰器里的参数是/user/，所以URL如上：127.0.0.1:5000/user
# 注意：建议在自定义URL的最后面都加上/，这样即使在浏览器里不输入最后一个/，
# 程序也会把/重定向上去，但如果自定义URL的最后不加/，那么在输入时，
# 如果在URL的最后输入了/，flask是不会重定向的，那么就会报错