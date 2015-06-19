import os

REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR', '127.0.0.1')
REDIS_URL = "redis://{host}/0".format(host=REDIS_HOST)

REDIS_CHANNEL_PREFIX = 'anpl_'

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@{host}/backend".format(
    host=os.environ.get('POSTGRES_PORT_5432_TCP_ADDR', '127.0.0.1'))

SENTRY_TORNADO = None
SENTRY_DSN = None

try:
    from backend.local_settings import *
except ImportError as e:
    pass
