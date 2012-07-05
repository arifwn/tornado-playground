
import os

import tornado.httpclient
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/index.html", title="Tornado", hello="Hello World!")


class TestErrorHandler(tornado.web.RequestHandler):
    def get(self):
        raise tornado.web.HTTPError(505)


class TestJsonOutputHandler(tornado.web.RequestHandler):
    def get(self):
        # dict are automatically serialized into json! apply to write, finish, etc...?
        data = {"json": "cool", "number": 1}
        self.write(data)


class TestAsyncHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        http = tornado.httpclient.AsyncHTTPClient()
        http.fetch("http://friendfeed-api.com/v2/feed/bret",
                   callback=self.on_response)

    def on_response(self, response):
        if response.error:
            raise tornado.web.HTTPError(500)
            
        entries = tornado.escape.json_decode(response.body)
        self.write("Fetched " + str(len(entries["entries"])) + " entries "
                   "from the FriendFeed API")
        self.finish()
        

settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    "login_url": "/login",
    "xsrf_cookies": True,
    "static_path": os.path.join(os.path.dirname(__file__), "static"),
    "debug": True,
}

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/async", TestAsyncHandler),
    (r"/error", TestErrorHandler),
    (r"/json", TestJsonOutputHandler),
], **settings)

def main():
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
    