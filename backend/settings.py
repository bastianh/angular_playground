import os

REDIS_URL = "redis://localhost/0"
REDIS_CHANNEL_PREFIX = 'anpl_'

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@{POSTGRES_HOST}/backend".format(
    POSTGRES_HOST=os.environ.get('POSTGRES_PORT_5432_TCP_ADDR', '127.0.0.1'))

SENTRY_TORNADO = None
SENTRY_DSN = None

try:
    from backend.local_settings import *
except ImportError as e:
    pass
