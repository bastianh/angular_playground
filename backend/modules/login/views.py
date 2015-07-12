from flask import session, url_for, redirect, render_template, current_app, request, abort

from flask.ext.login import login_required, current_user

from backend import settings
from backend.models.user import UserSchema, User
from backend.modules.login import bp
from backend.modules.login.forms import DebugLoginForm
from backend.signals import on_init_app
from backend.utils.database import db
from backend.utils.websignature import sign_dict


@on_init_app.connect
def init_app(app):
    app.add_url_rule('/', 'index', index)


def index():
    if current_user.is_authenticated():
        user = UserSchema(only=('character_id', 'character_name', 'id')).dump(current_user).data
        user = sign_dict(user, current_app.config["SECRET_KEY"])
        return render_template("index.html", user=user)
    form = None
    if current_app.debug:
        form = DebugLoginForm()
    return render_template("login.html", form=form)


@bp.route("/debug_login", methods=["POST"])
def debug_login():
    if not current_app.debug:
        abort(404)
    form = DebugLoginForm(request.form)
    if form.validate():
        provider_id = str(form.character_id)
        user = db.session.query(User).filter_by(provider_id=provider_id).filter_by(
            provider_name='debug').first()
        if not user:
            # noinspection PyArgumentList
            user = User.create(commit=False, provider_id=provider_id, provider_name='debug', admin=True)
        user.character_id = form.character_id
        user.character_name = form.character_name
        user.save()
        user.login()
        return redirect(url_for("index"))

    return render_template("login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    session.clear()
    current_user.logout()
    return redirect(url_for("index"))
