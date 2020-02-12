# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM


from flask import render_template, request
from app import db
from app.errors import bp
from app.api.errors import error_response as api_error_response


# 为错误响应进行内容协商
def wants_json_response():  # 函数对JSON和HTML格式比较友好
    return request.accept_mimetypes['application/json'] >= request.accept_mimetypes['text/html']


@bp.app_errorhandler(404)  # 该装饰球使blueprint独立于应用，使其更具可移植性。
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template('errors/500.html'), 500
