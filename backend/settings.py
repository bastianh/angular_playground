import logging

LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


TWOBADSSO = {
    'consumer_key':'test',
    'consumer_secret':'test',
}

REDIS_URL = "redis://localhost/0"

SQLALCHEMY_DATABASE_URI = "postgresql://vagrant:vagrant@localhost/backend"

try:
    from backend.local_settings import *
    logging.info("local settings loaded")
except ImportError as e:
    logging.warning("no local settings loaded")
    pass


