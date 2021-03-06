# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/31 2:32 PM


# 注册自定义应用命令
#
# 命令行增强功能，所以现在工作流程就简便多了，而且不需要记住长而复杂的命令。
#
# 要添加新的语言，请使用：
# (venv) $ flask translate init <language-code>
#
# 在更改_()和_l()语言标记后更新所有语言：
# (venv) $ flask translate update
#
# 在更新翻译文件后编译所有语言：
# (venv) $ flask translate compile
# """

import os
import click


def register(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        # translate为子命令的跟，通过app.cli.group()装饰器创建，为子命令提供基础
        pass

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d app/translations -l ' + lang):
            raise RuntimeError('init command failed')
        # os.remove('messages.pot')

    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d app/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d app/translations'):
            raise RuntimeError('compile command failed')
