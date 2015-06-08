#!/usr/bin/env python
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("manage.py")

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from backend.server import create_app
from backend.utils.database import db

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def run_tornado(debug=False):
    from backend.tornado import create_app
    import tornado
    application = create_app(debug)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(9999)
    logger.info("tornado gestartet (debug:%r)", debug)
    tornado.ioloop.IOLoop.instance().start()

@manager.command
def test():
    pass

if __name__ == "__main__":
    manager.run()
