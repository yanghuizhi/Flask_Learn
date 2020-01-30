import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'  # 密钥
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
        or 'sqlite:///' + os.path.join(basedir, 'app.db')   # 数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = False                  # 数据发生变更之后是否发送信号给应用
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')         # 日志

    # 邮件模块, 若.env未配置，则禁用电子邮件功能
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['your-email@example.com']

    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')  # Elasticsearch
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'
    POSTS_PER_PAGE = 3  # 用户动态分页
    LANGUAGES = ['zh', 'en', 'zh_Hans_CN']  # 语言explore