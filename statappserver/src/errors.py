from flask import jsonify


class AppException(Exception):
    status_code = 500
    detail = ''
    code = ''

    def __init__(self, detail=None, status_code=None, code=None, payload=None):
        Exception.__init__(self) # why we do this ???
        if detail:
            self.detail = detail
        if status_code is not None:
            self.status_code = status_code
        if code:
            self.code = code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['detail'] = self.detail
        rv['code'] = self.code
        return rv


class Unauthorized(AppException):
    status_code = 401
    detail = 'Authentication credentials are not provided'
    code = 'unauthorized'


class Forbidden(AppException):
    status_code = 403
    detail = 'Permission denied'
    code = 'forbidden'


def error_handler(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response