from flask.helpers import get_debug_flag

from src.configs import DebugConfig, ProdConfig
from src.app import create_app

conf_class = DebugConfig if get_debug_flag() else ProdConfig

app = create_app(conf_class)

if __name__ == '__main__':
    app.run(debug=True)