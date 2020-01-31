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
    """
    如果登录URL中不含next参数，那么将会重定向到本应用的主页。
    如果登录URL中包含next参数，其值是一个相对路径（换句话说，该URL不含域名信息），那么将会重定向到本应用的这个相对路径。
    如果登录URL中包含next参数，其值是一个包含域名的完整URL，那么重定向到本应用的主页。

    前两种情况很好理解，第三种情况是为了使应用更安全。
    攻击者可以在next参数中插入一个指向恶意站点的URL，因此应用仅在重定向URL是相对路径时才执行重定向，这可确保重定向与应用保持在同一站点中。
    为了确定URL是相对的还是绝对的，我使用Werkzeug的url_parse()函数解析，然后检查netloc属性是否被设置。
    """
    if current_user.is_authenticated:  # 检查用户是否登录
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():  # form 校验，如果请求是get，则返回false，跳过此代码段
        user = User.query.filter_by(username=form.username.data).first()
        # filter_by() 包含具有匹配用户名的对象的查询结果集。存在则返回用户对象;如果不存在则返回None
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)        # 注册为已登录
        next_page = request.args.get('next')                    # 未登录用户访问时被@login_required检测，进行重定向
        if not next_page or url_parse(next_page).netloc != '':  # 检查 netloc 属性是否被设置
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


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    # 创建一个视图函数专门用来处理密码重置函数
    if current_user.is_authenticated: # 用户若登录，重定向主页
        return redirect(url_for('main.index'))
    form = ResetPasswordRequestForm() # 调用函数
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password_request.html',
                           title=_('Reset Password'), form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    # 重置用户密码
    # 当用户点击电子邮件链接时，会触发与此功能相关的第二个路由。
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
