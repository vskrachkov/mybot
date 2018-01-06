from flask import current_app, request

from .errors import Unauthorized


@current_app.before_request
def before_request():
    if not request.authorization:
        raise Unauthorized()
    print('before request: ', request.authorization)