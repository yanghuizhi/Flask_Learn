# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2019/10/29 3:58 PM

"""
数据库模块, 构建用户信息模型

"""
from werkzeug.security import generate_password_hash, check_password_hash  # 哈希的两种方法
from datetime import datetime
from app import db
from flask_login import UserMixin
from app import login
from hashlib import md5  # 用户头像
from time import time
import jwt  # 密码重置安全令牌，比较流行的包
from app import app


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """
        用户可以在无需持久化存储原始密码的条件下执行安全的密码验证
        :param password:
        :return: 将用户输入的密码转换成哈希值
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        用户可以在无需持久化存储原始密码的条件下执行安全的密码验证
        :param password:
        :return: 将用户输入的密码和后台的哈希值进行校验
        """
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        """
        添加用户头像专用，链接中有两个参数如下：
            s = 尺寸大小，填写80就是 80x80
            d = 让Gravatar为没有向服务注册头像的用户提供的随机头像
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def follow(self, user): # 关注
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user): # 取消关注
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user): # 检查两个用户之间是否存在关系
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


@login.user_loader
def load_user(id):  # 用户加载函数
    """
    Flask-Login通过在用户会话中存储其唯一标识符来跟踪登录用户。每当已登录的用户导航到新页面时，Flask-Login将从会话中检索用户的ID，然后将该用户实例加载到内存中。
    使用Flask-Login的@login.user_loader装饰器来为用户加载功能注册函数。 Flask-Login将字符串类型的参数id传入用户加载函数，因此使用数字ID的数据库需要如上所示地将字符串转换为整数。
    get_id(): 返回用户的唯一id的方法，返回值类型是字符串(Python 2下返回unicode字符串).
    """
    return User.query.get(int(id))


class Post(db.Model): # 数据库表名
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
