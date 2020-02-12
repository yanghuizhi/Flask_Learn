from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

# 错误响应
def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
    if message:
        payload['message'] = message
    response = jsonify(payload)
    response.status_code = status_code
    return response

# 错误请求的响应
def bad_request(message):
    return error_response(400, message)
