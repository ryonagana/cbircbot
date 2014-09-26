import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

from threading import Thread



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")



class Server(Thread):

	def __init__(self):
		super().__init__()


	def initServer(self):
		self.app = tornado.web.Application(handlers=[(r'/',MainHandler)])
		self.http_server=tornado.httpserver.HTTPServer(self.app)
		self.http_server.listen(8888)

	def start(self):
		tornado.ioloop.IOLoop.instance().start()