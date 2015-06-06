from flask import session, url_for, request, jsonify, redirect, render_template
from flask.ext.login import LoginManager, login_required, current_user
from flask.ext.oauthlib.client import OAuth, OAuthException

from backend.database import db
from backend.models.user import User, UserSchema

from backend.signals import on_init_app

oauth = OAuth()
login_manager = LoginManager()

twobad = oauth.remote_app('twobad',
                          request_token_params={'scope': 'email'},
                          base_url='https://2bad.co/index.php/oauth/',
                          request_token_url=None,
                          access_token_method='POST',
                          access_token_url='https://2bad.co/index.php/oauth/token',
                          authorize_url='https://2bad.co/index.php/oauth/authorize',
                          app_key="TWOBADSSO",
                          )


@login_manager.user_loader
def load_user(userid):
    return User.get_user_for_session(userid)


@twobad.tokengetter
def get_twobad_oauth_token():
    return session.get('twobad_token')


@on_init_app.connect
def init_app(app):
    oauth.init_app(app)
    login_manager.init_app(app)

    @app.route("/")
    def index():
        user = None
        if current_user.is_authenticated():
            user = UserSchema(exclude=('email', 'provider_id', 'provider_name')).dump(current_user).data
        return render_template("index.html", user=user)


    @app.route('/login/twobad')
    def twobad_login_redirect():
        return twobad.authorize(callback=url_for('authorized', _external=True))

    @app.route('/login/authorized')
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
            user.login()
            return redirect(url_for(".index"))
        return jsonify(me.data)

    @app.route("/logout")
    @login_required
    def logout():
        session.clear()
        current_user.logout()
        return redirect(url_for("index"))
