from flask import request
import os
from backend.signals import on_init_app

_cache = {}

def static_file_hash(filename):
    val = _cache.get(filename, 0)
    if not val:
        try:
            val = _cache[filename] = int(os.stat(filename).st_mtime)
        except:
            pass
    return val

@on_init_app.connect
def init_flask_tools(app):
    @app.url_defaults
    def hashed_url_for_static_file(endpoint, values):
        if 'static' == endpoint or endpoint.endswith('.static'):
            filename = values.get('filename')
            if filename:
                #if '.' in endpoint:  # has higher priority
                #    blueprint = endpoint.rsplit('.', 1)[0]
                #else:
                #    blueprint = request.blueprint  # can be None too

                #if blueprint:
                #    static_folder = app.blueprints[blueprint].static_folder
                #else:
                static_folder = app.static_folder

                param_name = 'h'
                while param_name in values:
                    param_name = '_' + param_name
                values[param_name] = static_file_hash(os.path.join(static_folder, filename))
