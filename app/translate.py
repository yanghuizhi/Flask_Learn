# !/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: yanghuizhi
# Time: 2020/1/31 2:32 PM


import json
import requests
from flask import current_app
from flask_babel import _


# 文本翻译函数（目前市面上都是收费的，此功能未实现，有空的话用百度AI改造下试试）

def translate(text, source_language, dest_language):
    if 'MS_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    auth = {
        'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY']}
    r = requests.get('https://api.microsofttranslator.com/v2/Ajax.svc'
                     '/Translate?text={}&from={}&to={}'.format(
                         text, source_language, dest_language),
                     headers=auth)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(r.content.decode('utf-8-sig'))


# 该函数定义需要翻译的文本、源语言和目标语言为参数，并返回翻译后文本的字符串。 它首先检查配置中是否存在翻译服务的Key，如果不存在，则会返回错误。 错误也是一个字符串，所以从外部看，这将看起来像翻译文本。 这可确保在出现错误时用户将看到有意义的错误消息。
#
# requests包中的get()方法向作为第一个参数给定的URL发送一个带有GET方法的HTTP请求。 我使用*/v2/Ajax.svc/Translate* URL，它是翻译服务中的一个端点，它将翻译内容荷载为JSON返回。文本、源语言和目标语言都需要在URL中分别命名为text，from和to作为查询字符串参数。 要使用该服务进行身份验证，我需要将我添加到配置中的Key传递给该服务。 该Key需要在名为Ocp-Apim-Subscription-Key的自定义HTTP头中给出。 我创建了auth字典，然后将它通过headers参数传递给requests。
#
# requests.get()方法返回一个响应对象，它包含了服务提供的所有细节。 我首先需要检查和确认状态码是200，这是成功请求的代码。 如果我得到任何其他代码，我就知道发生了错误，所以在这种情况下，我返回一个错误字符串。 如果状态码是200，那么响应的主体就有一个带有翻译的JSON编码字符串，所以我需要做的就是使用Python标准库中的json.loads()函数将JSON解码为我可以使用的Python字符串。 响应对象的content属性包含作为字节对象的响应的原始主体，该属性是UTF-8编码的字符序列，需要先进行解码，然后发送给json.loads()。
#
# 下面你可以看到一个Python控制台会话，我演示了如何使用新的translate()函数：
#
# >>> from app.translate import translate
# >>> translate('Hi, how are you today?', 'en', 'es')  # English to Spanish
# 'Hola, ¿cómo estás hoy?'
# >>> translate('Hi, how are you today?', 'en', 'de')  # English to German
# 'Are Hallo, how you heute?'
# >>> translate('Hi, how are you today?', 'en', 'it')  # English to Italian
# 'Ciao, come stai oggi?'
# >>> translate('Hi, how are you today?', 'en', 'fr')  # English to French
# "Salut, comment allez-vous aujourd'hui ?"
# 很酷，对吧？ 现在是时候将此功能与应用集成在一起了。