from flask import Flask
# noinspection PyUnresolvedReferences
from flask.ext.login import current_user
from backend import settings
from backend.signals import on_init_app

# noinspection PyUnresolvedReferences
import backend.modules
from backend.utils.flask_tools import init_flask_tools


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    init_flask_tools(app)
    on_init_app.send(app)

    return app
