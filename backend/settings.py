TWOBADSSO = {
    'base_url': 'https://2bad.co/index.php/oauth/',
    'access_token_url': 'https://2bad.co/index.php/oauth/token',
    'authorize_url': 'https://2bad.co/index.php/oauth/authorize',
    'consumer_key': 'test',
    'consumer_secret': 'test',
}

REDIS_URL = "redis://localhost/0"
REDIS_CHANNEL_PREFIX = 'anpl_'

SQLALCHEMY_DATABASE_URI = "postgresql://vagrant:vagrant@localhost/backend"

try:
    from backend.local_settings import *
except ImportError as e:
    pass
