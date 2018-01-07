from functools import wraps

from flask import session

from src.errors import Unauthorized, Forbidden


class Permission:
    """Base permission class."""
    def has_permission(self):
        raise NotImplemented()


class OnlyAuthorizedPermission(Permission):
    """Only authorized users have access to resource"""
    def has_permission(self):
        user = session.get('user')
        if not user:
            raise Unauthorized()
        return True


def permissions(permissions_list):
    def wrapper(view_func):
        @wraps(view_func)
        def wrapped():
            check_permissions(permissions_list)
            return view_func

        return wrapped

    return wrapper


def check_permissions(permissions_list):
    for permission in permissions_list:
        has = permission().has_permission()
        if not has:
            raise Forbidden()