from flask import request, jsonify, session

from src.permissions import permissions, OnlyAuthorizedPermission
from .blueprint import metrics


@metrics.route('/weight', methods=['get', 'post'])
@permissions([OnlyAuthorizedPermission])
def weight():
    if request.method == 'POST':
        # save metric
        pass
    else:
        # list metric values
        return jsonify({'list': {'user': session['user']}})