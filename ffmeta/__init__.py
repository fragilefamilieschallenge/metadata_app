import os
from flask import Flask, jsonify
from ffmeta import settings
from ffmeta.blueprints import cache

app = Flask('ffmeta')


def create_app(debug=False):

    global app

    def handle_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    app.config.from_pyfile('settings.py')

    # The Flask App can also be configured (to override what is found in settings.py)
    # using environment variables, by prefixing the envvar name with 'FFMETA_'.
    # This prefix is stripped off before passing on to the Flask app.
    env_vars = {k[len('FFMETA_'):]: v for k, v in os.environ.items() if k.startswith('FFMETA_')}

    app.config.from_mapping(**env_vars)

    cache.init_app(app, config={'CACHE_TYPE': 'simple'})

    if debug:
        from werkzeug.debug import DebuggedApplication
        app.wsgi_app = DebuggedApplication(app.wsgi_app, True)

    import ffmeta.blueprints.web
    import ffmeta.blueprints.api2

    app.register_blueprint(ffmeta.blueprints.web.bp, url_prefix='/')
    app.register_blueprint(ffmeta.blueprints.api2.bp, url_prefix='/api')
    app.register_blueprint(ffmeta.blueprints.api2.bp, url_prefix='/', subdomain='api')

    from ffmeta.utils import AppException
    app.register_error_handler(AppException, handle_error)
    app.teardown_appcontext_funcs = (shutdown_session, )
    return app


def shutdown_session(exception=None):
    from ffmeta.models.db import session
    session.remove()
