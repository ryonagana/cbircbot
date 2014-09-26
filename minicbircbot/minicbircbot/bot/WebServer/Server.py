import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
from tornado import gen
from tornado.web import asynchronous


from threading import Thread



class MainHandler(tornado.web.RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self):
        self.write("Hello, world")



class Server(Thread):

	def __init__(self):
		super().__init__()
		self.app = tornado.web.Application(handlers=[(r'/',MainHandler)])
		self.http_server=tornado.httpserver.HTTPServer(self.app)
		self.http_server.listen(8888)



	def run(self):
		tornado.ioloop.IOLoop.instance().start()


	def stop(self):
		tornado.ioloop.IOLoop.instance().stop()
		self.join()


if __name__ == "__main__":
	s = Server()
	s.start()