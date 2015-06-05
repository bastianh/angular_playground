from flask import Flask, render_template, url_for, request, session, jsonify, redirect
from flask.ext.oauthlib.client import OAuth, OAuthException
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.debug = True
app.secret_key = 'development'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

db = SQLAlchemy(app)
oauth = OAuth(app)

twobad = oauth.remote_app(
    'twobad',
    consumer_key='test',
    consumer_secret='test',
    request_token_params={'scope': 'email'},
    base_url='https://2bad.co/index.php/oauth/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://2bad.co/index.php/oauth/token',
    authorize_url='https://2bad.co/index.php/oauth/authorize'
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route('/login')
def login():
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
        session["user"] = me.data["user"]
        return redirect(url_for(".index"))
    return jsonify(me.data)


@twobad.tokengetter
def get_twobad_oauth_token():
    return session.get('twobad_token')


if __name__ == "__main__":
    app.run(debug=True)
