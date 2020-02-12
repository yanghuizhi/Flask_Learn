from flask import Blueprint

bp = Blueprint('api', __name__)

from app.api import users, errors, tokens

# 简易版测试API
#
# 安装HTTPie，这是一个用Python编写的命令行HTTP客户端，可以轻松发送API请求：
# (venv) $ pip install httpie
#
# 查看用户1（请到最后携带token）
# http GET http://localhost:5000/api/users/1
# 注册新用户（请到最后携带token）
# http POST http://localhost:5000/api/users username=alice password=dog \
#     email=alice@example.com "about_me=Hello, my name is Alice!"
# 修改用户2的about_me字段（请到最后携带token）
# http PUT http://localhost:5000/api/users/2 "about_me=Hi, I am Miguel"
#
# 为了简化使用token认证时客户端和服务器之间的交互，我将使用名为Flask-HTTPAuth的Flask插件。 Flask-HTTPAuth可以使用pip安装：
#
# (venv) $ pip install flask-httpauth
#
# 获取token
# http --auth <username>:<password> POST http://localhost:5000/api/tokens
# http --auth 1:1 POST http://localhost:5000/api/tokens
# "token": "QBrX2uL8sGuODK4koKKqIw3b9tjdYD0j"

# 发送不记名token的格式
# http GET http://localhost:5000/api/users/1 \

# 这是从HTTPie发送的令牌撤销请求示例：
# http DELETE http://localhost:5000/api/tokens \
# Authorization:"Bearer pC1Nu9wwyNt8VCj1trWilFdFI276AcbS"

# 携带token 查看api
# http GET http://localhost:5000/api/users/1 \
# "Authorization:Bearer QBrX2uL8sGuODK4koKKqIw3b9tjdYD0j"