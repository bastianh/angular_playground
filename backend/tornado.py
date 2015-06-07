import json
import time
import logging

import jws

import tornado.httpserver
import tornado.web
import tornado.websocket
import tornado.ioloop
import tornado.gen
import redis
import tornadoredis
import tornadoredis.pubsub

from backend import settings
from backend.utils.websignature import check_dict

logger = logging.getLogger(__name__)

try:
    import sockjs.tornado
except:
    print('Please install the sockjs-tornado package to run this demo.')
    exit(1)


# Use the synchronous redis client to publish messages to a channel
redis_client = redis.Redis()
# Create the tornadoredis.Client instance
# and use it for redis channel subscriptions

class MySubscriber(tornadoredis.pubsub.SockJSSubscriber):
    def subscribe(self, channel_name, subscriber, callback=None):
        logger.debug("subscribe %r %r %r", channel_name, subscriber, callback)
        if isinstance(channel_name, list) or isinstance(channel_name, tuple):
            channel_name = ['%s%s' % (settings.REDIS_CHANNEL_PREFIX, name) for name in channel_name]

        super().subscribe(channel_name, subscriber, callback)

    def get_subscribers(self, channel_name):
        logger.debug("get_subscribers %r", channel_name)
        return list(subscriber.subscribers['%s%s' % (settings.REDIS_CHANNEL_PREFIX, channel_name)].keys())

    def unsubscribe(self, channel_name, subscriber):
        logger.warn("unsubscribe %r", channel_name, subscriber)
        super().unsubscribe(channel_name, subscriber)

    def unsubscribe_all_channels(self, subscriber):
        for channel_name, subscribers in self.subscribers.items():
            if subscribers:
                if subscriber in subscribers.keys():
                    super().unsubscribe(channel_name, subscriber)

    def publish(self, channel_name, data, client=None, callback=None):
        logger.warn("publish %r %r %r %r", channel_name, data, client, callback)
        super().publish(channel_name, data, client, callback)

    def on_message(self, msg):
        logger.debug("on_message %r", msg)
        super().on_message(msg)

    def is_subscribed(self):
        logger.debug("is_subscribed")
        return super().is_subscribed()

    def close(self):
        logger.debug("close")
        super().close()


subscriber = MySubscriber(tornadoredis.Client())


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("template.html", title="PubSub + SockJS Demo")


class SendMessageHandler(tornado.web.RequestHandler):
    def _send_message(self, channel, msg_type, msg, user=None):
        msg = {'type': msg_type,
               'msg': msg,
               'user': user}
        msg = json.dumps(msg)
        redis_client.publish(channel, msg)

    def post(self):
        message = self.get_argument('message')
        from_user = self.get_argument('from_user')
        to_user = self.get_argument('to_user')
        if to_user:
            self._send_message('private.{}'.format(to_user),
                               'pvt', message, from_user)
            self._send_message('private.{}'.format(from_user),
                               'tvp', message, to_user)
        else:
            self._send_message('broadcast_channel', 'msg', message, from_user)
        self.set_header('Content-Type', 'text/plain')
        self.write('sent: %s' % (message,))


class MessageHandler(sockjs.tornado.SockJSConnection):
    """
    SockJS connection handler.
    Note that there are no "on message" handlers - SockJSSubscriber class
    calls SockJSConnection.broadcast method to transfer messages
    to subscribed clients.
    """

    def _enter_leave_notification(self, msg_type):
        broadcasters = subscriber.get_subscribers('broadcast_channel')
        message = json.dumps({'type': msg_type,
                              'user': self.user_id,
                              'msg': '',
                              'user_list': {b.user_id: {'character_name': b.user['character_name'],
                                                        'character_id': b.user['character_id']} for b in broadcasters}})

        if broadcasters:
            broadcasters[0].broadcast(broadcasters, message)

    def _send_message(self, msg_type, msg, user=None):
        if not user:
            user = self.user_id
        self.send(json.dumps({'type': msg_type,
                              'msg': msg,
                              'user': user}))

    def on_message(self, message):
        message = json.loads(message)
        if 'user' in message:
            if hasattr(self, 'user_id'):
                return
            user = message['user']
            try:
                user = check_dict(user, settings.SECRET_KEY)
            except jws.exceptions.SignatureError as e:
                self.close()
                logging.warning("signatur error %r %r", e, user)
                return
            logger.debug("user %r", user)
            self.user_id = user['id']
            self.user = user
            subscriber.subscribe(['broadcast_channel'], self)
            self._enter_leave_notification('enters')
            logger.debug("SUBSCRIBER %r", subscriber.get_subscribers('broadcast_channel'))

    def _add_authcheck_timeout(self):
        io_loop = tornado.ioloop.IOLoop.instance()
        self._authcheck_timeout = io_loop.add_timeout(time.time() + 15, self._authcheck)

    def _authcheck(self):
        if not hasattr(self, 'user_id'):
            logger.warning("disconnecting unknown connection %r", self)
            self.close()
        del self._authcheck_timeout

    def on_open(self, request):
        self._add_authcheck_timeout()

    def on_close(self):
        if hasattr(self, '_authcheck_timeout'):
            tornado.ioloop.IOLoop.current().remove_timeout(self._authcheck_timeout)
        # subscriber.unsubscribe('private.{}'.format(self.user_id), self)
        # subscriber.unsubscribe('broadcast_channel', self)
        ## Send the 'user leaves the chat' notification
        # self._enter_leave_notification('leaves')
        logger.info("disconnected %r", self)
        logger.debug("SUBSCRIBER %r", subscriber.get_subscribers('broadcast_channel'))
        subscriber.unsubscribe_all_channels(self)


def create_app(debug=False):
    application = tornado.web.Application(
        [(r'/', IndexPageHandler),
         (r'/send_message', SendMessageHandler)] +
        sockjs.tornado.SockJSRouter(MessageHandler, '/sockjs').urls,
        autoreload=debug, compiled_template_cache=debug,
        serve_traceback=debug)
    return application
