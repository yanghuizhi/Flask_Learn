# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/31 2:32 PM


import base64
from datetime import datetime, timedelta
from hashlib import md5
import json
import os
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import redis
import rq
from app import db, login
from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):  # 搜索类
    @classmethod
    def search(cls, expression, page, per_page):  # 将id列表转化成实例对象
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):  # SQLAlchemy事件，事件之前触发
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):  # SQLAlchemy事件，事件之后触发
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):  # 帮助方法，刷新所有数据索引
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


# Post模型会自动为用户动态维护一个全文搜索索引。
# 这两行代码设置了每次提交之前和之后调用的事件处理程序。
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


class PaginatedAPIMixin(object):  # 分页表示mixin类，API用
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        # 产生一个带有用户集合表示的字典
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data

# 粉丝机制关联表
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, PaginatedAPIMixin, db.Model):  # 用户表
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))   # 保存用户密码的哈希值
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))        # 个人资料编辑器
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)  # 记录用户的最后访问时间
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    # 粉丝机制表中的关系
    # 建立关系的过程实属不易。 就像我为post一对多关系所做的那样，我使用db.relationship函数来定义模型类中的关系。
    # 这种关系将User实例关联到其他User实例，所以按照惯例，对于通过这种关系关联的一对用户来说，左侧用户关注右侧用户。 我在左侧的用户中定义了followed的关系，因为当我从左侧查询这个关系时，我将得到已关注的用户列表（即右侧的列表）。 让我们逐个检查这个db.relationship()所有的参数：
    # 'User'是关系当中的右侧实体（将左侧实体看成是上级类）。由于这是自引用关系，所以我不得不在两侧都使用同一个实体。
    # secondary 指定了用于该关系的关联表，就是使用我在上面定义的followers。
    # primaryjoin 指明了通过关系表关联到左侧实体（关注者）的条件 。关系中的左侧的join条件是关系表中的follower_id字段与这个关注者的用户ID匹配。followers.c.follower_id表达式引用了该关系表中的follower_id列。
    # secondaryjoin 指明了通过关系表关联到右侧实体（被关注者）的条件。这个条件与primaryjoin类似，唯一的区别在于，现在我使用关系表的字段的是followed_id了。
    # backref定义了右侧实体如何访问该关系。在左侧，关系被命名为followed，所以在右侧我将使用followers来表示所有左侧用户的列表，即粉丝列表。附加的lazy参数表示这个查询的执行模式，设置为动态模式的查询不会立即执行，直到被调用，这也是我设置用户动态一对多的关系的方式。
    # lazy和backref中的lazy类似，只不过当前的这个是应用于左侧实体，backref中的是应用于右侧实体。
    # 如果理解起来比较困难，你也不必过于担心。我待会儿就会向你展示如何利用这些关系来执行查询，一切就会变得清晰明了。
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    # User模型对私有消息的支持，发送消息/接收消息
    # 这两个关系将返回给定用户发送和接收的消息，并且在关系的Message一侧将添加author和recipient回调引用。 我之所以使用author回调而不是更适合的sender，是因为通过使用author，我可以使用我用于用户动态的相同逻辑渲染这些消息。 last_message_read_time字段将存储用户最后一次访问消息页面的时间，并将用于确定是否有比此字段更新时间戳的未读消息。 new_messages()
    # 辅助方法实际上使用这个字段来返回用户有多少条未读消息。 在本章的最后，我将把这个数字作为页面顶部导航栏中的一个漂亮的徽章。
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author', lazy='dynamic')
    messages_received = db.relationship('Message',
                                        foreign_keys='Message.recipient_id',
                                        backref='recipient', lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)
    # 通知模型
    notifications = db.relationship('Notification', backref='user',
                                    lazy='dynamic')
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def __repr__(self):  # 调试时打印用户实例
        return '<User {}>'.format(self.username)


    # 通过werkzeug.security, 进行设置密码 和 检查密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    # 粉丝机制中，添加和删除关注关系的代码变更
    def follow(self, user):  # 关注对方
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):  # 取消关注对方
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):  # 判断是否重复关注
        """
        这里使用的filter()方法很类似，但是更加偏向底层，因为它可以包含任意的过滤条件，而不像filter_by()，它只能检查是否等于一个常量值。 我在is_following()中使用的过滤条件是，查找关联表中左侧外键设置为self用户且右侧设置为user参数的数据行。 查询以count()方法结束，返回结果的数量。 这个查询的结果是0或1，因此检查计数是1还是大于0实际上是
        """
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):  # 查看已关注用户的动态
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def avatar(self, size):  # 用户头像
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


    # 通过JWT生成密码重置邮件密钥，验证时在反过来验证密钥
    def get_reset_password_token(self, expires_in=600):
        # JWT令牌生成方式
        # jwt.encode()函数将令牌作为字节序列返回，但是在应用中将令牌表示为字符串更方便
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)


    def new_messages(self):  # 私有消息支持
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()

    def add_notification(self, name, data):
        # Notification模型辅助方法，以便更轻松地处理这些对象
        self.notifications.filter_by(name=name).delete()
        n = Notification(name=name, payload_json=json.dumps(data), user=self)
        db.session.add(n)
        return n

    # 用户模型中的任务辅助方法
    # launch_task()方法负责将任务提交到RQ队列，并将其添加到数据库中。 name参数是函数名称，如app/tasks.py中所定义的那样。 提交给RQ时，该函数会将app.tasks.预先添加到该名称中以构建符合规范的函数名称。description参数是对呈现给用户的任务的友好描述。 对于导出用户动态的函数，我将名称设置为export_posts，将描述设置为Exporting posts...。 其余参数将传递给任务函数。 launch_task()函数首先调用队列的enqueue()方法来提交作业。 返回的作业对象包含由RQ分配的任务ID，因此我可以使用它在我的数据库中创建相应的Task对象。
    #
    # 请注意，launch_task()将新的任务对象添加到会话中，但不会发出提交。 一般来说，最好在更高层次函数中的数据库会话上进行操作，因为它允许你在单个事务中组合由较低级别函数所做的多个更新。 这不是一个严格的规则，并且，在本章后面的子函数中也会存在一个例外的提交。
    #
    # get_tasks_in_progress()方法返回该用户未完成任务的列表。 稍后你会看到，我使用此方法在将有关正在运行的任务的信息渲染到用户的页面中。
    #
    # 最后，get_task_in_progress()是上一个方法的简化版本并返回指定的任务。 我阻止用户同时启动两个或多个相同类型的任务，因此在启动任务之前，可以使用此方法来确定前一个任务是否还在运行。
    def launch_task(self, name, description, *args, **kwargs):
        rq_job = current_app.task_queue.enqueue('app.tasks.' + name, self.id, *args, **kwargs)
        task = Task(id=rq_job.get_id(), name=name, description=description, user=self)
        db.session.add(task)
        return task

    def get_tasks_in_progress(self):
        return Task.query.filter_by(user=self, complete=False).all()

    def get_task_in_progress(self, name):
        return Task.query.filter_by(name=name, user=self, complete=False).first()

    # User模型转换成表示，使用json包将数据返回成字典
    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'username': self.username,
            'last_seen': self.last_seen.isoformat() + 'Z',
            'about_me': self.about_me,
            'post_count': self.posts.count(),
            'follower_count': self.followers.count(),
            'followed_count': self.followed.count(),
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'followers': url_for('api.get_followers', id=self.id),
                'followed': url_for('api.get_followed', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    # 表示转换成User模型
    def from_dict(self, data, new_user=False):
        for field in ['username', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    # 支持用户token, API用
    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


@login.user_loader
def load_user(id):
    # 每当已登录的用户导航到新页面时，Flask-Login将从会话中检索用户的ID
    return User.query.get(int(id))  # 传入字符串类型，使用数字ID的数据库需要将字符串转换为整数。


class Post(SearchableMixin, db.Model):  # 发布用户状态表
    __searchable__ = ['body']
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # timestamp = db.Column(db.DateTime, index=True, default=datetime.strptime(t,"%Y-%m-%d %H:%M:%S").date())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 用户表ID
    language = db.Column(db.String(5))  # 监测用户语言

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Message(db.Model):  # 发送私有消息
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 发信人
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 收信人
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)


class Notification(db.Model):  # 通知模型，用户消息通知
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):  # 调用者不必操心JSON的反序列化
        return json.loads(str(self.payload_json))


class Task(db.Model):  # Task模型
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    complete = db.Column(db.Boolean, default=False)

    def get_rq_job(self):
        try:
            rq_job = rq.job.Job.fetch(self.id, connection=current_app.redis)
        except (redis.exceptions.RedisError, rq.exceptions.NoSuchJobError):
            return None
        return rq_job

    def get_progress(self):
        job = self.get_rq_job()
        return job.meta.get('progress', 0) if job is not None else 100
