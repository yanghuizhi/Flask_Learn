from app import create_app, db, cli
from app.models import User, Post, Message, Notification, Task

app = create_app()
cli.register(app)  # 巧妙的方法注册cli


@app.shell_context_processor  # 此装饰器会将函数注册为 shell 上下文函数
def make_shell_context():
    """
    运行 flask shell 时, 调用该函数并返回注册的项目, 函数返回一个字典格式.
    """
    return {'db': db, 'User': User, 'Post': Post,
            'Message': Message, 'Notification': Notification, 'Task': Task}

print(make_shell_context.__dict__)