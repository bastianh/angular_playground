#!/usr/bin/env python
import logging

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from backend import settings

from backend.server import create_app
from backend.database import db

logging.basicConfig(format=settings.LOG_FORMAT, level=settings.LOG_LEVEL)

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def hello():
    print("hello")


if __name__ == "__main__":
    manager.run()
