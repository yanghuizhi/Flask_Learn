#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Post
from app.config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'  # 覆盖SQLAlchemy配置以使用内存SQLite数据库
    ELASTICSEARCH_URL = None


class UserModelCase(unittest.TestCase):
    def setUp(self):  # 为每次测试创建一个应用
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from john", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)

# 新的应用将存储在self.app中，但光是创建一个应用不足以使所有的工作都成功。 思考创建数据库表的db.create_all()语句。 db实例需要注册到应用实例，因为它需要从app.config获取数据库URI，但是当你使用应用工厂时，应用就不止一个了。 那么db如何关联到我刚刚创建的self.app实例呢？
#
# 答案在application context中。 还记得current_app变量吗？当不存在全局应用实例导入时，该变量以代理的形式来引用应用实例。 这个变量在当前线程中查找活跃的应用上下文，如果找到了，它会从中获取应用实例。 如果没有上下文，那么就没有办法知道哪个应用实例处于活跃状态，所以current_app就会引发一个异常。 下面你可以看到它是如何在Python控制台中工作的。 这需要通过运行python启动，因为flask shell命令会自动激活应用程序上下文以方便使用。
#
# >>> from flask import current_app
# >>> current_app.config['SQLALCHEMY_DATABASE_URI']
# Traceback (most recent call last):
#     ...
# RuntimeError: Working outside of application context.
#
# >>> from app import create_app
# >>> app = create_app()
# >>> app.app_context().push()
# >>> current_app.config['SQLALCHEMY_DATABASE_URI']
# 'sqlite:////home/miguel/microblog/app.db'
#
# 这就是秘密所在！ 在调用你的视图函数之前，Flask推送一个应用上下文，它会使current_app和g生效。 当请求完成时，上下文将与这些变量一起被删除。 为了使db.create_all()调用在单元测试setUp()方法中工作，我为刚刚创建的应用程序实例推送了一个应用上下文，这样db.create_all()可以使用 current_app.config知道数据库在哪里。 然后在tearDown()方法中，我弹出上下文以将所有内容重置为干净状态。
#
# 你还应该知道，应用上下文是Flask使用的两种上下文之一，还有一个请求上下文，它更具体，因为它适用于请求。 在处理请求之前激活请求上下文时，Flask的request、session以及Flask-Login的current_user变量才会变成可用状态。