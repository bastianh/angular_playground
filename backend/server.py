from flask import Flask
from flask.ext.admin import Admin
from werkzeug import import_string
# noinspection PyUnresolvedReferences
from flask.ext.login import current_user

from backend import settings
from backend.modules.maintain.views import Supervisor
from backend.signals import on_init_app


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    # import modules listed in config file
    for module in settings.LOAD_MODULES:
        import_string(module)

    # send init signal
    on_init_app.send(app)
    return app


def create_debug_app():
    import werkzeug
    from sqltap.wsgi import SQLTapMiddleware

    app = create_app()
    app.debug = True
    app.wsgi_app = SQLTapMiddleware(app.wsgi_app)
    # noinspection PyUnresolvedReferences
    app = werkzeug.DebuggedApplication(app, evalex=True)
    return app

def create_maintain_app():

    app = Flask(__name__)
    app.config.from_object(settings)
    app.debug = True

    admin = Admin(app=app, url="/", template_mode='bootstrap3')
    admin.add_view(Supervisor(name='Supervisor'))

    return app
