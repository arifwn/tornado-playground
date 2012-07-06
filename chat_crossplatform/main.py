
import logging
import os

import tornado.escape
import tornado.httpclient
import tornado.ioloop
import tornado.web
import tornado.websocket


participants_comet = set()
participants_websocket = set()


class MainWebsocketHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/websocket.html")


class MainCometHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/comet.html")


class MessageHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        global participants_comet
        participants_comet.add(self)
    
    def send_message(self, message):
        if self.request.connection.stream.closed():
            return
        
        self.finish(message)


class NewMessageHandler(tornado.web.RequestHandler):
    
    def post(self):
        global participants_comet
        message = { "name": self.get_argument("name", "anonymous"),
                   "message": self.get_argument("message", "")}
        for participant in participants_comet:
            try:
                participant.send_message(message)
            except:
                logging.error("Error in participant callback", exc_info=True)
        
        participants_comet = set()
        
        global participants_websocket
        for participant in participants_websocket:
            participant.write_message(message)
        
        self.write(message)


class MessageWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        global participants_websocket
        participants_websocket.add(self)

    def on_message(self, message_str):
        message_dict = tornado.escape.json_decode(message_str)
        message = { "name": message_dict.get("name", "anonymous"),
                   "message": message_dict.get("message", "")}
        
        global participants_comet
        for participant in participants_comet:
            try:
                participant.send_message(message)
            except:
                logging.error("Error in participant callback", exc_info=True)
        
        participants_comet = set()
        
        global participants_websocket
        for participant in participants_websocket:
            participant.write_message(message)

    def on_close(self):
        global participants_websocket
        participants_websocket.remove(self)


settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,
}

application = tornado.web.Application([
    (r"/", MainWebsocketHandler),
    (r"/comet", MainCometHandler),
    (r"/messagesocket", MessageWebSocket),
    (r"/cometmessage", MessageHandler),
    (r"/cometnewmessage", NewMessageHandler),
], **settings)

def main():
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
    