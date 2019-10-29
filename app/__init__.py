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

from flask import Flask

app = Flask(__name__)
app.run(debug=True)  # 开启 Debug 模式

from app import routes


