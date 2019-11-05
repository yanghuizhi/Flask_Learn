# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2019/10/29 2:13 PM

"""
    其一，这里有两个实体名为app。
    app包由app目录和__init__.py脚本来定义构成，并在from app import routes语句中被引用。
    app变量被定义为__init__.py脚本中的Flask类的一个实例，以至于它成为app包的属性。

    其二，routes模块是在底部导入的，而不是在脚本的顶部。
    最下面的导入是解决循环导入的问题，这是Flask应用程序的常见问题。
    你将会看到routes模块需要导入在这个脚本中定义的app变量，因此将routes的导入放在底部可以避免由于这两个文件之间的相互引用而导致的错误。
"""

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy  # Flask扩展, 数据库配置
from flask_migrate import Migrate
from flask_login import LoginManager  # 管理用户的登录状态，即保持登录
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel  # 简化翻译工作
from flask import request
from flask_babel import lazy_gettext as _l  # 翻译，简化其命名方式


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'  # 登录认证，登录成功后才可以进入
mail= Mail(app)  # 邮件实例化
bootstrap = Bootstrap(app)
moment = Moment(app)  # 使用moment.js并管理时间
babel = Babel(app)
login.login_message = _l('Please log in to access this page.')


@babel.localeselector  # 每个请求调用装饰器函数以选择用于该请求的语言
def get_locale():
    # return request.accept_languages.best_match(app.config['LANGUAGES'])
    return 'en'  # 直接定义语言

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')

from app import routes, models, errors
