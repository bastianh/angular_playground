from flask import request, url_for, jsonify, session, redirect
from flask.ext.oauthlib.client import OAuthException

from backend.models.user import User
from backend.modules.login import oauth, bp
from backend.utils.database import db

twobad = oauth.remote_app('twobad',
                          base_url='https://2bad.co/index.php/oauth/',
                          access_token_url='https://2bad.co/index.php/oauth/token',
                          authorize_url='https://2bad.co/index.php/oauth/authorize',
                          request_token_params={'scope': 'skipconfirm'},
                          request_token_url=None,
                          access_token_method='POST',
                          app_key="TWOBADSSO",
                          )


@twobad.tokengetter
def get_twobad_oauth_token():
    return session.get('twobad_token')


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
