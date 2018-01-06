def authenticate(username, user_id):
    """Performs user authentication.
    Also handle case when user change username.

    :param username: username provided by Telegram Api
    :param user_id: user id provided by Telegram Api
    :returns: core.User object
    """
    return {'username': username, 'id': user_id}