from app import create_app, db, cli
from app.models import User, Post, Message, Notification, Task

app = create_app()
cli.register(app)  # 巧妙的方法注册cli


@app.shell_context_processor  # 将函数注册为一个shell上下文函数
def make_shell_context():
    """
    flask shell命令运行时, 调用该函数并返回注册的项目
    """
    return {'db': db, 'User': User, 'Post': Post, 'Message': Message,
            'Notification': Notification, 'Task': Task}

print(make_shell_context.__dict__)