from contextlib import contextmanager
import logging
import os
from urllib.parse import urlsplit
from alembic import command
from alembic.config import Config
from flask import current_app
from flask.ext.admin import expose
from flask.ext.migrate import Migrate
from psycopg2 import connect

from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from six import StringIO
from backend.utils.database import db
from maintain.modules.baseclass import MaintainBaseView
from maintain.signals import get_admin_modules


@contextmanager
def dbcon():
    url = urlsplit(current_app.config['SQLALCHEMY_DATABASE_URI'])
    user, host = url[1].split("@")
    user, password = user.split(":")
    con = connect(user=user, host=host, password=password)
    try:
        yield con
    finally:
        con.close()


@get_admin_modules.connect
def init_app(app):
    return Database(name='Database'), 90


class Database(MaintainBaseView):
    @expose("/")
    def index(self):
        return self.render('database/index.html')

    @expose('/upgrade')
    def upgrade(self):
        Migrate(current_app, db)
        directory = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "migrations")
        config = Config()
        config.set_main_option("script_location", directory)
        stream = StringIO()
        handler = logging.StreamHandler(stream)
        # sqlalchemy_logger = logging.getLogger("sqlalchemy")
        alembic_logger = logging.getLogger("alembic")
        alembic_logger.setLevel(logging.DEBUG)
        alembic_logger.addHandler(handler)
        # sqlalchemy_logger.setLevel(logging.DEBUG)
        # sqlalchemy_logger.addHandler(handler)
        command.upgrade(config, "head")
        handler.flush()
        alembic_logger.removeHandler(handler)
        # sqlalchemy_logger.removeHandler(handler)
        handler.close()
        out = stream.getvalue()
        stream.close()
        return "<code>%s</code>" % out.replace("\n", "<br>")

    @expose('/createdb')
    def createdb(self):
        url = urlsplit(current_app.config['SQLALCHEMY_DATABASE_URI'])
        dbname = url[2][1:]
        with dbcon() as con:
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            with con.cursor() as cur:
                cur.execute('CREATE DATABASE "%s"' % dbname)

        return str(url)
