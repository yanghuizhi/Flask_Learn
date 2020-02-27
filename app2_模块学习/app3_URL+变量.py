# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/2/26 4:15 下午

# coding=utf-8
from flask import Flask, url_for

# 创建了一个Flask类的实例__name__是自定义的名称，也可以用其他的，如__main__等
app = Flask(__name__)

@app.route("/user/<id>")  # 用route()装饰器来自定义自己的URL
def re_id(id):  # 创建一个函数，返回一个值
    return "hello user%d" % int(id)


if __name__ == '__main__':
    app.debug = True
    app.run()

# 这个写法的区别在于return语句，例子中的return语句是用%d完成的，这里注意，URL中的传参默认都是str类型的，如果你按这种写法，也就是说，当你需要返回一个int类型的id时，必须把id转成int类型。
#
# URL中加的变量可以有五种类型，说明如下：
#
# 各个参数类型及释义：
#
# 类型            释义
# —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— —— —
# string     此项为默认值，如果你不输入类型，默认就是它，它接受任何文本，除了/
# int        正整数
# float      浮点数
# path       类似于string，但可以包含/
# uuid       接受uuid字符串
#
# uuid释义：uuid是国际通行的唯一标识码，它是纯数字的，它保证在同一时空中，任何一次生成的uuid码都是唯一的，开放软件基金会对它进行了定义，它包含有时间，时间、以太网地址、CPU的id等各种数字。