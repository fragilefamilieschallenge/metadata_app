import os.path
from flask import Flask, jsonify

from ffmeta import settings
from ffmeta.utils import AppException
from ffmeta.blueprints import cache


def create_app(debug=False):

    import ffmeta

    def handle_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    app = Flask('ffmeta')
    app.config.from_pyfile('settings.py')
    cache.init_app(
        app,
        config={
            'CACHE_TYPE': 'filesystem',
            'CACHE_DIR': os.path.join(os.path.dirname(ffmeta.__file__), app.config['CACHE_DIR'])
        }
    )

    if debug:
        from werkzeug.debug import DebuggedApplication
        app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

    import ffmeta.blueprints.web
    import ffmeta.blueprints.api
    import ffmeta.blueprints.api2

    app.register_blueprint(ffmeta.blueprints.web.bp, url_prefix='/')
    app.register_blueprint(ffmeta.blueprints.api.bp, url_prefix='/', subdomain='api')
    app.register_blueprint(ffmeta.blueprints.api2.bp, url_prefix='/api')
    app.register_blueprint(ffmeta.blueprints.api2.bp, url_prefix='/', subdomain='api')

    app.register_error_handler(AppException, handle_error)
    app.teardown_appcontext_funcs = (shutdown_session, )
    return app


def shutdown_session(exception=None):
    from ffmeta.models.db import session
    session.remove()
