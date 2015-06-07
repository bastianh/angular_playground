# coding=utf-8
from redis import StrictRedis
from backend.signals import on_init_app


class OurRedis(object):

    def __init__(self):
        pass

    def init_app(self, app):

        self.connection = connection = StrictRedis.from_url(app.config["REDIS_URL"])
        self._include_connection_methods(connection)


    def _include_connection_methods(self, connection):
        """
        Include methods from connection instance to current instance.
        """
        for attr in dir(connection):
            value = getattr(connection, attr)
            if attr.startswith('_') or not callable(value):
                continue
            self.__dict__[attr] = value

redis = OurRedis()
""":type: StrictRedis""" # hint for pycharm

@on_init_app.connect
def on_app_initialize(app):
    # flask extension initialisieren
    redis.init_app(app)
