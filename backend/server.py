from flask import Flask, url_for
from werkzeug import import_string
# noinspection PyUnresolvedReferences
from flask.ext.login import current_user

from backend import settings
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
    from werkzeug.wsgi import DispatcherMiddleware
    app = Flask(__name__)
    app.config.from_object(settings)
    app.config['APPLICATION_ROOT'] = "/_mt"

    @app.route("/")
    def hello_world():
        import xmlrpc.client
        proxy = xmlrpc.client.ServerProxy("http://localhost:9001/RPC2")
        return str(proxy.supervisor.getAllConfigInfo())

    app = DispatcherMiddleware(app,{ "/_mt" : app})
    return app
