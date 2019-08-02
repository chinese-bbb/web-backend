from flask import Flask


def create_app(**kwargs):
    """
    Entry point to the Flask RESTful Server application
    ===================================================
    """
    # This is a workaround for Alpine Linux (musl libc) quirk:
    # https://github.com/docker-library/python/issues/211
    # import threading

    # threading.stack_size(2 * 1024 * 1024)

    from config import Config

    app = Flask(__name__, **kwargs)

    app.config.from_object(Config)

    from . import extensions

    extensions.init_app(app)

    from . import resources

    resources.init_app(app)

    from app.extensions import blueprint
    from app.home import bp as home_blueprint

    app.register_blueprint(blueprint, url_prefix='/api')
    app.register_blueprint(home_blueprint, url_prefix='/')

    return app
