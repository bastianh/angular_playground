from flask import session, Blueprint
from flask.ext.login import LoginManager
from flask.ext.oauthlib.client import OAuth

from backend.models.user import User
from backend.signals import on_init_app

oauth = OAuth()
login_manager = LoginManager()

bp = Blueprint('login', __name__, url_prefix="/login")

import backend.modules.login.evesso
import backend.modules.login.twobadsso
import backend.modules.login.views


@login_manager.user_loader
def load_user(userid):
    return User.get_user_for_session(userid)


@on_init_app.connect
def init_app(app):
    oauth.init_app(app)
    login_manager.init_app(app)
    app.register_blueprint(bp)
