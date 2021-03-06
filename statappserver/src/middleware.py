from flask import current_app, request, session

from .authentication import authenticate


@current_app.before_request
def before_request():
    authentication_middleware()


def authentication_middleware():
    auth = request.authorization
    if not auth:
        session['user'] = None
        return

    username = auth.get('username')
    user_id = auth.get('password')

    session['user'] = authenticate(username, user_id)
