# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/2/10 4:24 下午


# 我准备自己加网页，自己写，先留作计划吧
# 有空再来

from flask import Blueprint

bp = Blueprint('yhz', __name__)

from app.my_yhzlearn import routes
