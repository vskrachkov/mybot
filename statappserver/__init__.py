from flask.helpers import get_debug_flag

from .configs import DebugConfig, ProdConfig
from .app import create_app

conf_class = DebugConfig if get_debug_flag() else ProdConfig

app = create_app(conf_class)