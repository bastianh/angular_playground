from flask import session, url_for, redirect, request

from backend.models.user import User
from backend.modules.login import bp, oauth
from backend.utils.database import db

evesso = oauth.remote_app('evesso',
                          base_url='https://login.eveonline.com/oauth/',
                          access_token_url='https://login.eveonline.com/oauth/token',
                          access_token_method='POST',
                          authorize_url='https://login.eveonline.com/oauth/authorize',
                          app_key='EVESSO')


@evesso.tokengetter
def get_evesso_oauth_token():
    return session.get('evesso_token')


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

    provider_id = "%r%r" % (user_data['CharacterID'], user_data['CharacterOwnerHash'])
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
