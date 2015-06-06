import inspect

from dogpile.cache import make_region
from dogpile.cache import compat
from backend import settings
from backend.signals import on_init_app


def function_key_generator(namespace, fn, to_str=compat.string_type):
    if namespace is None:
        namespace = '%s:%s' % (fn.__module__, fn.__name__)
    else:
        namespace = '%s:%s|%s' % (fn.__module__, fn.__name__, namespace)

    args = inspect.getargspec(fn)
    has_self = args[0] and args[0][0] in ('self', 'cls')

    def generate_key(*fargs, **kw):
        if kw:
            kwa = "|%r" % kw
        else:
            kwa = ""
        if has_self:
            fargs = fargs[1:]
        # print namespace + "|" + " ".join(map(to_str, args)) + kwa
        key = namespace + "|" + " ".join(map(to_str, fargs)) + kwa
        return key
        # return hashlib.sha224(key.encode('utf-8')).hexdigest()

    return generate_key


rediscache = make_region(function_key_generator=function_key_generator)

@on_init_app.connect
def on_app_initialize(app):
    try:
        rediscache.configure(
            'dogpile.cache.redis',
            arguments={
                'url': settings.REDIS_URL,
                'redis_expiration_time': 60 * 60 * 24 * 7,  # 7 days
                'distributed_lock': True
            })
    except Exception as e:
        print("%r" % e)
