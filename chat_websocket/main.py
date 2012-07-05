
import logging
import os

import tornado.httpclient
import tornado.ioloop
import tornado.web
import tornado.websocket


participants = set()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html")


class MessageWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        global participants
        participants.add(self)

    def on_message(self, message):
        global participants
        for participant in participants:
            participant.write_message(message)

    def on_close(self):
        global participants
        participants.remove(self)


settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/messagesocket", MessageWebSocket),
], **settings)

def main():
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
    