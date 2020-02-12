# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/31 2:32 PM


from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

# 电子邮件框架 - 异步函数
def send_email(subject, sender, recipients, text_body, html_body,
               attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
            args=(current_app._get_current_object(), msg)).start()

# 在send_email()函数中，应用实例作为参数传递给后台线程，后台线程将发送电子邮件而不阻塞主应用程序。在作为后台线程运行的send_async_email()函数中直接使用current_app将不会奏效，因为current_app是一个与处理客户端请求的线程绑定的上下文感知变量。在另一个线程中，current_app没有赋值。直接将current_app作为参数传递给线程对象也不会有效，因为current_app实际上是一个代理对象，它被动态地映射到应用实例。因此，传递代理对象与直接在线程中使用current_app相同。我需要做的是访问存储在代理对象中的实际应用程序实例，并将其作为app参数传递。 current_app._get_current_object()表达式从代理对象中提取实际的应用实例，所以它就是我作为参数传递给线程的。

# Message类的attach()方法接受三个定义附件的参数：文件名，媒体类型和实际文件数据。 文件名就是收件人看到的与附件关联的名称。 媒体类型定义了这种附件的类型，这有助于电子邮件读者适当地渲染它。 例如，如果你发送image/png作为媒体类型，则电子邮件阅读器会知道该附件是一个图像，在这种情况下，它可以显示它。 对于用户动态数据文件，我将使用JSON格式，该格式使用application/json媒体类型。 最后一个参数包含附件内容的字符串或字节序列。
#
# 简单来说，send_email()的attachments参数将成为一个元组列表，每个元组将有三个元素对应于attach()的三个参数。 因此，我需要将此列表中的每个元素作为参数发送给attach()。 在Python中，如果你想将列表或元组中的每个元素作为参数传递给函数，你可以使用func(*args)将这个列表或元祖解包成函数中的多个参数，而不必枯燥地一个个地传递，如func(args[0], args[1], args[2])。 例如，如果你有一个列表args = [1, 'foo']，func(*args)将会传递两个参数，就和你调用func(1, 'foo')一样。 如果没有*，调用将会传入一个参数，即args列表。
#
# 至于电子邮件的同步发送，我需要做的就是，当sync是True的时候恢复成调用mail.send(msg)。