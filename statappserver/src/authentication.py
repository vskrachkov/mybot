from src.core.models import User


def authenticate(username, user_id):
    """Performs user authentication.
    Also handle case when user change username.

    :param username: username provided by Telegram Api
    :param user_id: user id provided by Telegram Api
    :returns: core.User object
    """
    user = User.query.filter_by(telegram_id=user_id).first()
    return user