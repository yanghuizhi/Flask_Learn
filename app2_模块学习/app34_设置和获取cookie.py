# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM

# 设置cookie
from flask import Flask,make_response
@app.route('/cookie')
def set_cookie():
    resp = make_response('this is to set cookie')
    resp.set_cookie('username', 'itcast')
    return resp



from flask import Flask,request
#获取cookie
@app.route('/request')
def resp_cookie():
    resp = request.cookies.get('username')
    return resp