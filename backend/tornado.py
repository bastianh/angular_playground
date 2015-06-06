from tornado import web, ioloop
from sockjs.tornado import SockJSRouter, SockJSConnection

class EchoConnection(SockJSConnection):
    def on_message(self, msg):
        self.send(msg)
