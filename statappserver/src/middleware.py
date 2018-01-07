from flask import current_app, request, session

from .authentication import authenticate
from .errors import Unauthorized


@current_app.before_request
def before_request():
    authentication_middleware()


def authentication_middleware():
    auth = request.authorization
    if not auth:
        raise Unauthorized()

    username = auth.get('username')
    user_id = auth.get('password')

    user = authenticate(username, user_id)

    if not user:
        raise Unauthorized()

    session['user'] = user
