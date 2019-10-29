# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2019/10/29 2:14 PM

from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"