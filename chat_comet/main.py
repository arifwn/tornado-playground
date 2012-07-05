
import logging
import os

import tornado.httpclient
import tornado.ioloop
import tornado.web


participants = set()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html")


class MessageHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        global participants
        participants.add(self.on_new_message)
    
    def on_new_message(self, name, message):
        if self.request.connection.stream.closed():
            return
        
        message = { "name": name, "message": message}
        self.finish(message)


class NewMessageHandler(tornado.web.RequestHandler):
    
    def post(self):
        global participants
        name = self.get_argument("name")
        message = self.get_argument("message")
        for callback in participants:
            try:
                callback(name, message)
            except:
                logging.error("Error in participant callback", exc_info=True)
        
        participants = set()
        self.write({"name": name, "message": message})


settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/message", MessageHandler),
    (r"/newmessage", NewMessageHandler),
], **settings)

def main():
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
    