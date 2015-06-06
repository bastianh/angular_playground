import logging

from flask import Flask, render_template
# noinspection PyUnresolvedReferences
from flask.ext.login import current_user
from backend import settings, modules
from backend.models.user import UserSchema
from backend.signals import on_init_app


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    on_init_app.send(app)

    @app.route("/")
    def index():
        user = None
        if current_user.is_authenticated():
            user = UserSchema(exclude=('email','provider_id','provider_name')).dump(current_user).data
            user["te'st"] = 'hey"ho\'sd'
        return render_template("index.html", user=user)

    return app

