from flask import render_template, request
from app import db
from app.errors import bp
from app.api.errors import error_response as api_error_response


def wants_json_response():
    return request.accept_mimetypes['application/json'] >= \
        request.accept_mimetypes['text/html']

# 放弃使用@app.errorhandler装饰器将错误处理程序附加到应用程序，而是使用blueprint的@bp.app_errorhandler装饰器。
# 尽管两个装饰器最终都达到了相同的结果，但这样做的目的是试图使blueprint独立于应用，使其更具可移植性。
# 我还需要修改两个错误模板的路径，因为它们被移动到了新errors子目录。

@bp.app_errorhandler(404)
def not_found_error(error):
    if wants_json_response():
        return api_error_response(404)
    return render_template('errors/404.html'), 404


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    if wants_json_response():
        return api_error_response(500)
    return render_template('errors/500.html'), 500
