from flask import request

from .blueprint import metrics


@metrics.route('/weight', methods=['get', 'post'])
def weight():
    if request.method == 'POST':
        # save metric
        pass
    else:
        # list metric values
        return 'Weight list'