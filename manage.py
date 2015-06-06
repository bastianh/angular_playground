#!/usr/bin/env python
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from backend.server import create_app
from backend.database import db

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def tornado():
    from tornado import web, ioloop
    from sockjs.tornado import SockJSRouter
    from backend.tornado import EchoConnection

    EchoRouter = SockJSRouter(EchoConnection, '/echo')

    app = web.Application(EchoRouter.urls)
    app.listen(9999)
    ioloop.IOLoop.instance().start()



if __name__ == "__main__":
    manager.run()
