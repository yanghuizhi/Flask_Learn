# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/21 6:58 PM


from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes


# # 主应用Blueprint
#
# 第三个blueprint包含核心应用逻辑。
# 重构这个blueprint和前两个blueprint的过程一样。
# 我给这个blueprint命名为main，
# 因此所有引用视图函数的url_for()调用都必须添加一个main.前缀。
# 鉴于这是应用的核心功能，我决定将模板留在原来的位置。
# 这不会有什么问题，因为我已将其他两个blueprint中的模板移动到子目录中了。