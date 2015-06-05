#!/usr/bin/env python

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from backend.server import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def hello():
    print("hello")


if __name__ == "__main__":
    manager.run()
