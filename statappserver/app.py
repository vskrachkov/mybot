from flask import Flask


def create_app(config_class):
    """App factory for building Flask application.

    :param config_class: class that holds app configuration values
    """
    # create a Flask application instance
    app = Flask(__name__.split('.')[0])

    # load configs
    app.config.from_object(config_class)

    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    register_shell_context(app)
    register_middleware(app)

    return app


def register_extensions(app):
    """Register application extensions.

    :param app: Flask application instance
    """
    # import all extensions instances
    from .extensions import db

    # register these extensions
    db.init_app(app)


def register_blueprints(app):
    """Register application blueprints.

    :param app: Flask application instance
    """
    # import blueprints instances
    from .core import core
    from .metrics import metrics
    from .keep import keep

    # register these blueprints
    app.register_blueprint(core)
    app.register_blueprint(metrics, url_prefix='/metrics')
    app.register_blueprint(keep, url_prefix='/keep')


def register_error_handlers(app):
    """Register error handlers."""
    with app.app_context():
        from . import errors


def register_shell_context(app):
    """Register application shell context objects."""
    from .extensions import db

    def shell_context():
        """Shell context objects."""
        return {'db': db, }

    app.shell_context_processor(shell_context)


def register_middleware(app):
    """Register request middleware."""
    with app.app_context():
        from . import middleware