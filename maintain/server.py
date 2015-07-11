from flask import Flask
from flask.ext.admin import Admin
import werkzeug
from backend import settings
from maintain.signals import on_init_maintain_app, get_admin_modules

MODULES = [
    'maintain.modules.database.views',
    'maintain.modules.maintain.views',
]


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)
    app.debug = True

    for module in MODULES:
        werkzeug.import_string(module)

    on_init_maintain_app.send(app)

    admin = Admin(app=app, url="/", template_mode='bootstrap3')

    for m in sorted([x for x in get_admin_modules.send(app) if x], key=lambda x: x[1][1]):
        admin.add_view(m[1][0])

    return app
