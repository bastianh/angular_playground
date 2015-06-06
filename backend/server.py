from flask import Flask
# noinspection PyUnresolvedReferences
from flask.ext.login import current_user
from backend import settings
from backend.signals import on_init_app

# noinspection PyUnresolvedReferences
import backend.modules

def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    on_init_app.send(app)

    return app
