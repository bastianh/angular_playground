from collections import OrderedDict
import string
import time

import random
import jws


def sign_dict(data, key):
    data['_salt'] = ''.join(
        random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(10))
    data['_time'] = int(time.time())
    data = OrderedDict(sorted(data.items()))
    data['_token'] = jws.sign({'alg': 'HS384'}, data, key).decode('utf-8')
    return data


def check_dict(data, key):
    """
    raises jws.exceptions.SignatureError if it fails
    :rtype: dict
    """
    token = data.get('_token')
    if not token:
        raise jws.exceptions.SignatureError("missing token!")
    signature = bytes(token, encoding='utf-8')
    del data['_token']
    data = OrderedDict(sorted(data.items()))
    jws.verify({'alg': 'HS384'}, data, signature, key)
    return data
