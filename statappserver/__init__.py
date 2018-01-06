from flask.helpers import get_debug_flag

from .app import create_app

conf_class = 0 if get_debug_flag() else 1

app = create_app(conf_class)