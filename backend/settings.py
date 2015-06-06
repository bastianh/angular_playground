
TWOBADSSO = {
    'consumer_key':'test',
    'consumer_secret':'test',
}

REDIS_URL = "redis://localhost/0"

SQLALCHEMY_DATABASE_URI = "postgresql://vagrant:vagrant@localhost/backend"

try:
    from backend.local_settings import *
except ImportError as e:
    pass


