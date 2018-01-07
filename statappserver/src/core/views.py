from flask import jsonify

from .blueprint import core


@core.route('/register', methods=['post'])
def registration():
    return jsonify({}), 201
