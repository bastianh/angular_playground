from io import StringIO
import logging
import os
from flask import request, current_app
from flask.ext.admin import AdminIndexView, Admin, expose

from backend.models.user import User
from backend.modules.admin import MyBaseView
from backend.modules.admin.models import UserView, ApiCallView
from backend.signals import on_init_app
from backend.utils.database import db
from backend.utils.eveapi import ApiCall


class MyView(MyBaseView):
    def is_accessible(self):
        return True

    @expose('/')
    def index(self):
        return self.render("admin/index.html", data="hello")

class Database(MyBaseView):

    def is_accessible(self):
        if request.endpoint == "database.setup":
            return True
        return super().is_accessible()

    @expose('/')
    def index(self):
        return "Database"

    @expose('/setup/<key>')
    def setup(self, key):
        return "KEY %r" % key
        from alembic.config import Config
        from alembic import command
        from flask.ext.migrate import Migrate
        Migrate(current_app, db)
        directory = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))),"migrations")
        config = Config()
        config.set_main_option("script_location", directory)
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        #sqlalchemy_logger = logging.getLogger("sqlalchemy")
        alembic_logger = logging.getLogger("alembic")
        alembic_logger.setLevel(logging.DEBUG)
        alembic_logger.addHandler(handler)
        #sqlalchemy_logger.setLevel(logging.DEBUG)
        #sqlalchemy_logger.addHandler(handler)
        command.upgrade(config, "head")
        handler.flush()
        alembic_logger.removeHandler(handler)
        #sqlalchemy_logger.removeHandler(handler)
        handler.close()
        out = stream.getvalue()
        stream.close()
        return "<code>%s</code>" % out.replace("\n","<br>")


class MyHomeView(AdminIndexView, MyBaseView):
    def is_accessible(self):
        return True

    @expose()
    def index(self):
        return self.render("admin/index.html", data=self._template)

@on_init_app.connect
def init_app(app):
    admin = Admin(app=app,index_view=MyHomeView(), template_mode='bootstrap2')
    admin.add_view(MyView(name='Hello'))
    admin.add_view(Database(name='Database'))
    admin.add_view(UserView(User, db.session, category="Models"))
    admin.add_view(ApiCallView(ApiCall, db.session, category="Models"))

