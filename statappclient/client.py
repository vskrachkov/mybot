import requests


__all__ = ['Client']


class Client:
    """Client for statistic app, that provide simple interface
    for statistics app API usage.
    Each client creates new connection with server, so do not
    create multiple Client instances if you do not really need this.
    """
    __version__ = '0.0.1'

    __password = 'rukivdupe'

    def __init__(self, secret):
        self.s = requests.Session()

        self.s.headers.update({'x-stat-app-client': self.__version__})
        self.s.headers.update({'x-stat-app-secret': secret})

    def auth(self, username):
        """

        :param username: username of the user for whom statistic
            you want take access.
        :return:
        """
        self.s.auth = (username, self.__password)

    def push_metric(self, metric_name, data):
        """

        :param metric_name: name of the metric on the server
        :param data: dictionary with metric values
        :return: None if all fine or message with error details
        """
        return 'Server are not available for now'

    def get_metric(self, metric_name):
        """

        :param metric_name:
        :return: dictionary with metric values
        """
        return
