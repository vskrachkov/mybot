from flask import current_app, request, session

from .authentication import authenticate
from .errors import Unauthorized


@current_app.before_request
def before_request():
    auth = request.authorization
    if not auth and not current_app.debug:
        raise Unauthorized()

    username = auth.get('username')
    user_id = auth.get('password')

    session['user'] = authenticate(username, user_id)