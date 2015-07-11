from flask import Flask
import werkzeug
# noinspection PyUnresolvedReferences
from flask.ext.login import current_user

from backend import settings
from backend.signals import on_init_app


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    # import modules listed in config file
    for module in settings.LOAD_MODULES:
        werkzeug.import_string(module)

    # send init signal
    on_init_app.send(app)

    if app.debug:
        from sqltap.wsgi import SQLTapMiddleware
        app.wsgi_app = SQLTapMiddleware(app.wsgi_app)
        # noinspection PyUnresolvedReferences
        app = werkzeug.DebuggedApplication(app, evalex=True)
    return app
