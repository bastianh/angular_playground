from flask import session, url_for, request, jsonify, redirect, render_template, Blueprint
from flask.ext.login import LoginManager, login_required, current_user

from flask.ext.oauthlib.client import OAuth, OAuthException

from backend import settings
from backend.utils.database import db
from backend.models.user import User, UserSchema
from backend.signals import on_init_app
from backend.utils.websignature import sign_dict

oauth = OAuth()
login_manager = LoginManager()

evesso = oauth.remote_app('evesso',
                          base_url='https://login.eveonline.com/oauth/',
                          access_token_url='https://login.eveonline.com/oauth/token',
                          access_token_method='POST',
                          authorize_url='https://login.eveonline.com/oauth/authorize',
                          app_key='EVESSO')

twobad = oauth.remote_app('twobad',
                          request_token_params={'scope': 'skipconfirm'},
                          request_token_url=None,
                          access_token_method='POST',
                          app_key="TWOBADSSO",
                          )


@login_manager.user_loader
def load_user(userid):
    return User.get_user_for_session(userid)


@twobad.tokengetter
def get_twobad_oauth_token():
    return session.get('twobad_token')

@evesso.tokengetter
def get_evesso_oauth_token():
    return session.get('evesso_token')

bp = Blueprint('login', __name__, url_prefix="/login")

@on_init_app.connect
def init_app(app):
    oauth.init_app(app)
    login_manager.init_app(app)

    app.register_blueprint(bp)
    app.add_url_rule('/', 'index', index)

def index():
    if current_user.is_authenticated():
        user = UserSchema(only=('character_id', 'character_name', 'id')).dump(current_user).data
        user = sign_dict(user, settings.SECRET_KEY)
        return render_template("index.html", user=user)
    return render_template("login.html")

@bp.route('/twobad')
def twobad_login_redirect():
    return twobad.authorize(callback=url_for('.authorized', _external=True))

@bp.route('/authorized')
def authorized():
    resp = twobad.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error'],
            request.args['error_description']
        )
    if isinstance(resp, OAuthException):
        return 'Access denied: %r' % resp
    session['twobad_token'] = (resp['access_token'], '')
    me = twobad.get('me')
    if me.data["success"]:
        user_data = me.data["user"]
        user = db.session.query(User).filter_by(provider_id=user_data['user_id']).filter_by(
            provider_name='2bad').first()
        if not user:
            # noinspection PyArgumentList
            user = User.create(commit=False, provider_id=user_data['user_id'], provider_name='2bad')
        user.character_id = user_data["character_id"]
        user.character_name = user_data["username"]
        user.save()
        user.login()
        return redirect(url_for("index"))
    return jsonify(me.data)

@bp.route("/evesso")
def evesso_login_redirect():
    return evesso.authorize(callback=url_for('.evesso_authorized', _external=True, _scheme="https"))

@bp.route('/callback/eve')
def evesso_authorized():
    resp = evesso.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    if isinstance(resp, Exception):
        return 'Access denied: error=%s' % str(resp)

    session['evesso_token'] = (resp['access_token'], '')

    me = evesso.get("verify")
    user_data = me.data

    provider_id = int(user_data['CharacterID'])  # FIXME: TODO: sollte kein int sein  "%r%r" % (user_data['CharacterID'], user_data['CharacterOwnerHash'])
    user = db.session.query(User).filter_by(provider_id=provider_id).filter_by(
        provider_name='eve').first()
    if not user:
        # noinspection PyArgumentList
        user = User.create(commit=False, provider_id=provider_id, provider_name='eve')
    user.character_id = user_data["CharacterID"]
    user.character_name = user_data["CharacterName"]
    user.save()
    user.login()
    return redirect(url_for("index"))

@bp.route("/logout")
@login_required
def logout():
    session.clear()
    current_user.logout()
    return redirect(url_for("index"))
