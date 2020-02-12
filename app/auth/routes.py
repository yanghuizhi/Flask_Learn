# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM


from flask import render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from flask_babel import _
from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from app.models import User
from app.auth.email import send_password_reset_email


@bp.route('/login', methods=['GET', 'POST'])
def login():  # 用户登录
    if current_user.is_authenticated:  # 检查用户是否登录
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():  # 请求为Post、所有数据校验通过，置为True
        # 查询user对象，若无则None
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))  # 自动重定向参数关联的URL
        login_user(user, remember=form.remember_me.data)
        # 在用户通过调用Flask-Login的login_user()函数登录后，应用获取了next查询字符串参数的值。 Flask提供一个request变量，其中包含客户端随请求发送的所有信息。 特别是request.args属性，可用友好的字典格式暴露查询字符串的内容。 实际上有三种可能的情况需要考虑，以确定成功登录后重定向的位置：
        # 如果登录URL中不含next参数，那么将会重定向到本应用的主页。
        # 如果登录URL中包含next参数，其值是一个相对路径（换句话说，该URL不含域名信息），那么将会重定向到本应用的这个相对路径。
        # 如果登录URL中包含next参数，其值是一个包含域名的完整URL，那么重定向到本应用的主页。
        #
        # 前两种情况很好理解，第三种情况是为了使应用更安全。
        # 攻击者可以在next参数中插入一个指向恶意站点的URL，因此应用仅在重定向URL是相对路径时才执行重定向，这可确保重定向与应用保持在同一站点中。
        # 为了确定URL是相对的还是绝对的，我使用Werkzeug的url_parse()函数解析，然后检查netloc属性是否被设置。
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title=_('Sign In'), form=form)


@bp.route('/logout')
def logout():  # 用户登出
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():  # 用户注册
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():  # 验证通过则登录，否则注册
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title=_('Register'), form=form)


# 重置密码视图函数，第一个方法触发发送邮件，第二个方法实现更改密码
@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated: # 用户是否登录
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm() # 调用函数
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:  # 判断用户是否存在
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Reset Password'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
