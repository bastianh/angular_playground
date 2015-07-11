import os

from flask import Flask
from flask.ext.admin import Admin
import time
import werkzeug
from backend import settings
from backend.utils.config import INIConfig
from maintain.modules.home.views import HomeView
from maintain.signals import on_init_maintain_app, get_admin_modules

MODULES = [
    'maintain.modules.database.views',
    'maintain.modules.maintain.views',
]


def create_app():
    app = Flask(__name__)
    INIConfig(app=app)
    app.config.from_object(settings)
    app.config.from_inifile(settings.CONFIG_FILE, app=app)

    if not app.config.get("SECRET_KEY"):
        app.config['SECRET_KEY'] = str(time.ctime(os.path.getmtime(__file__)))
        app.config['TEMP_SECRET_KEY'] = True

    for module in MODULES:
        werkzeug.import_string(module)

    on_init_maintain_app.send(app)

    admin = Admin(app=app, index_view=HomeView(url="/"), template_mode='bootstrap3')

    for m in sorted([x for x in get_admin_modules.send(app) if x], key=lambda x: x[1][1]):
        admin.add_view(m[1][0])

    return app
