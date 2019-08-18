import json
import traceback
from http import HTTPStatus

from flask import Flask
from flask import request

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

    define_global_interception(app)

    return app


def define_global_interception(app):
    @app.errorhandler(Exception)
    def handle_global_exception(e):
        tb = traceback.format_exc()
        app.logger.error(
            '%s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
            request.remote_addr,
            request.method,
            request.scheme,
            request.full_path,
            tb,
        )

        return 'oohs! something goes wrong', HTTPStatus.INTERNAL_SERVER_ERROR

    @app.before_request
    def before():
        values = 'request values: '
        if len(request.data) > 0:
            data = json.loads(request.data)
            for key in data.keys():
                if 'password' in key:
                    data[key] = '**********'
            values += json.dumps(data)
            app.logger.debug(values)

    @app.after_request
    def after_request(response):
        app.logger.info(
            '%s %s %s %s %s -',
            request.remote_addr,
            request.scheme,
            request.method,
            request.full_path,
            response.status,
        )
        return response
