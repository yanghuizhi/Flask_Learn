import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request, current_app
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l # 翻译
from elasticsearch import Elasticsearch
from redis import Redis
import rq
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'  # 强制用户查看特定页面之前登录
login.login_message = _l('Please log in to access this page.')
mail = Mail()
bootstrap = Bootstrap() # css
moment = Moment() # 时间
babel = Babel() # 全局扫描提取翻译


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)  # 读取配置

    db.init_app(app)  # 数据库注册
    migrate.init_app(app, db)  # 数据库迁移引擎
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    babel.init_app(app)
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None
    app.redis = Redis.from_url(app.config['REDIS_URL'])
    app.task_queue = rq.Queue('microblog-tasks', connection=app.redis)

    """
    为了注册blueprint，将使用Flask应用实例的register_blueprint()方法。 
    在注册blueprint时，任何视图函数，模板，静态文件，错误处理程序等均连接到应用。
    将blueprint的导入放在app.register_blueprint()的上方，以避免循环依赖。
    """
    # 注册 app.errors
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    if not app.debug and not app.testing:
    # 仅当应用未以调试模式运行，且配置中存在邮件服务器时，我才会启用电子邮件日志记录器。
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'],
                        app.config['MAIL_PASSWORD'])
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

        if app.config['LOG_TO_STDOUT']:  # 记录日志到文件
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
            # RotatingFileHandler可以切割和清理日志文件，以确保日志文件在应用运行很长时间时不会变得太大。
            # 日志大小，保留最后的十个日志文件作为备份
            file_handler.setFormatter(logging.Formatter(  # 自定义格式
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)  # 等级
        app.logger.info('Microblog startup')

    return app


@babel.localeselector
def get_locale():
    # return request.accept_languages.best_match(current_app.config['LANGUAGES'])
    return 'zh' # 特殊的中文格式


from app import models  # 解决循环导入问题
