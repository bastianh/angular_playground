import os

DEBUG = os.environ.get('DEBUG_APP', False)

# application settings

LOAD_MODULES = [
    "backend.utils.ext",
    "backend.utils.flask_helper",
    "backend.utils.eveapi",
    "backend.modules",
    "backend.modules.admin.views"
]

SECRET_KEY = None

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),"config.ini")

# database / services

REDIS_HOST = os.environ.get('REDIS_PORT_6379_TCP_ADDR', '127.0.0.1')
REDIS_URL = "redis://{host}/0".format(host=REDIS_HOST)

REDIS_CHANNEL_PREFIX = 'anpl_'

SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@{host}/backend".format(
    host=os.environ.get('POSTGRES_PORT_5432_TCP_ADDR', '127.0.0.1'))

# sentry error reporting

SENTRY_TORNADO = None
SENTRY_DSN = None

# celery settings

BROKER_URL = REDIS_URL
CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']

try:
    from backend.local_settings import *
except ImportError as e:
    pass
