from flask import Flask

from app.extensions import api


def create_app(app_name, config_or_path=None, **kwargs):
    """
    Entry point to the Flask RESTful Server application
    ===================================================
    """
    # This is a workaround for Alpine Linux (musl libc) quirk:
    # https://github.com/docker-library/python/issues/211
    # import threading

    # threading.stack_size(2 * 1024 * 1024)

    app = Flask(app_name, **kwargs)

    try:
        app.config.from_object(config_or_path)
    except ImportError:
        raise

    from . import extensions

    extensions.init_app(app)

    from app.extensions import api_blueprint

    from . import resources

    resources.init_app(app, api_blueprint)

    from app.home import bp as home_blueprint

    api.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(home_blueprint, url_prefix='/')

    return app
