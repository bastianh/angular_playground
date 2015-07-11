from urllib.parse import urlsplit

from flask import current_app
from flask.ext.admin import BaseView, expose
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from maintain.signals import get_admin_modules


@get_admin_modules.connect
def init_app(app):
    return Database(name='Database'), 90


class Database(BaseView):
    def is_accessible(self):
        return True

    @expose('/createdb')
    def createdb(self):
        url = urlsplit(current_app.config['SQLALCHEMY_DATABASE_URI'])
        user, host = url[1].split("@")
        user, password = user.split(":")
        dbname = url[2][1:]
        con = connect(user=user, host=host, password=password)
        con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = con.cursor()
        cur.execute('CREATE DATABASE "%s"' % dbname)
        cur.close()
        con.close()

        return str(url)
