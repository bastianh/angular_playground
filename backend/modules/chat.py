# noinspection PyMethodMayBeStatic
import json

from flask import request
from flask.ext.classy import FlaskView
from flask.ext.login import login_required, current_user
import time

from backend import settings
from backend.signals import on_init_app
from backend.utils.redis_ext import redis

class ChatView(FlaskView):
    decorators = [login_required]

    def post(self):
        data = request.get_json(cache=False)
        message = {
            "user": current_user.id,
            "msg": data['message'],
            "type": "chat",
            "character_name": current_user.character_name,
            "character_id": current_user.character_id,
            "time": int(time.time() * 1000)
        }
        redis.publish('%sbroadcast_channel' % settings.REDIS_CHANNEL_PREFIX, json.dumps(message))
        return ""


@on_init_app.connect
def init_app(app):
    ChatView.register(app)
