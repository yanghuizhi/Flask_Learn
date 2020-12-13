# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM

from flask import Flask,abort
@app.route('/')
def hello_itcast():
    abort(404)
    return 'hello itcast',999

# 如果在视图函数执行过程中，出现了异常错误，我们可以使用abort函数立即终止视图函数的执行。通过abort函数，可以向前端返回一个http标准中存在的错误状态码，表示出现的错误信息。
#
# 使用abort抛出一个http标准中不存在的自定义的状态码，没有实际意义。如果abort函数被触发，其后面的语句将不会执行。其类似于python中raise。

"""
捕获异常：
在Flask中通过装饰器来实现捕获异常，errorhandler()接收的参数为异常状态码。视图函数的参数，返回的是错误信息。
"""

@app.errorhandler(404)  # 捕获上面的404
def error(e):
    return '您请求的页面不存在了，请确认后再次访问！%s'%e