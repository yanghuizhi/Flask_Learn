# 错误处理Blueprint

from flask import Blueprint

bp = Blueprint('errors', __name__)
# template_folder='templates'参数，则可以将错误blueprint的模板存储在app/errors/templates目录中。
from app.errors import handlers  # 该导入位于底部以避免循环依赖。

# 在Flask中，blueprint是代表应用子集的逻辑结构。
# blueprint可以包括路由，视图函数，表单，模板和静态文件等元素。
# 如果在单独的Python包中编写blueprint，那么你将拥有一个封装了应用特定功能的组件。
# Blueprint的内容最初处于休眠状态。
# 为了关联这些元素，blueprint需要在应用中注册。
# 在注册过程中，需要将添加到blueprint中的所有元素传递给应用。
# 因此，你可以将blueprint视为应用功能的临时存储，以帮助组织代码。

"""
app/
    errors/                             <-- blueprint package
        __init__.py                     <-- blueprint creation
        handlers.py                     <-- error handlers
    templates/
        errors/                         <-- error templates
            404.html
            500.html
    __init__.py                         <-- blueprint registration
"""