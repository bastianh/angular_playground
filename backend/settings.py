

REDIS_URL = "redis://localhost/0"
REDIS_CHANNEL_PREFIX = 'anpl_'

SQLALCHEMY_DATABASE_URI = "postgresql://vagrant:vagrant@localhost/backend"

try:
    from backend.local_settings import *
except ImportError as e:
    pass
