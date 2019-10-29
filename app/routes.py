# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2019/10/29 2:14 PM

"""
    视图函数
"""

from flask import render_template  # Flask 框架原生依赖的 Jinja2 模板引擎
from app import app
from forms import LoginForm
from flask import flash, redirect, url_for


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    form.validate_on_submit()实例方法进行form校验
        请求是get时，返回 False，并跳转视图函数最后一句渲染模版
        请求时post时，若验证通过，返回 True，
    flash() 函数是向用户显示消息的有效途径，但只能作为临时解决方案
    redirect() 函数指引浏览器自动重定向到它的参数所关联的URL，即回到主页
    """
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)