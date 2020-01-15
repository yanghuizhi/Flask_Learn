from app import create_app, db, cli
from app.models import User, Post, Message, Notification, Task

app = create_app()
cli.register(app)  # 巧妙的方法注册cli


@app.shell_context_processor  # 将函数注册为一个shell上下文函数
def make_shell_context():
    """
    flask shell命令运行时，它会调用这个函数并在shell会话中注册它返回的项目。
    :return:
    """
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            'Notification': Notification, 'Task': Task}
