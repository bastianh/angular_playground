from raven.contrib.flask import Sentry

from backend.signals import on_init_app

sentry = Sentry()


@on_init_app.connect
def init_app(app):
    sentry.init_app(app)
