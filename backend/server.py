from flask import Flask
# noinspection PyUnresolvedReferences
from flask.ext.login import current_user
from raven.contrib.flask import Sentry
from backend import settings
from backend.signals import on_init_app

# noinspection PyUnresolvedReferences
import backend.modules
from backend.utils.flask_tools import init_flask_tools

sentry = Sentry()

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    sentry.init_app(app)
    init_flask_tools(app)
    on_init_app.send(app)
    return app

def create_debug_app():
    import werkzeug
    app = create_app()
    app.debug = True
    # noinspection PyUnresolvedReferences
    app = werkzeug.DebuggedApplication(app, evalex=True)
    return app
