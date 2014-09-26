import os
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient
from tornado import gen
from tornado.web import asynchronous
from tornado.web import StaticFileHandler
import tornado.template

from threading import Thread


STATIC_PATH= os.path.join(os.getcwd(), 'web')
TEMPLATE_PATH = os.path.join(STATIC_PATH, 'templates')
template = tornado.template.Loader(STATIC_PATH)

class MainHandler(tornado.web.RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self):

    	self.render("index.html")


class MainHandler2(tornado.web.RequestHandler):
    @asynchronous
    @gen.coroutine
    def get(self):
        self.write("Hello,//Otavio")





class Server(Thread):




	def __init__(self, irc = None):
		super().__init__()

		self.irc = irc


		settings = {
		'debug': True, 
		'static_path': os.path.join(STATIC_PATH, 'assets'),
		'template_path':  TEMPLATE_PATH
		}

		handlers = [
		(r'/', MainHandler),
		(r'/otavio/', MainHandler2),


		(r'/static/(.*)',  tornado.web.StaticFileHandler, {'path': './assets' }),
		#(r'/(favicon\.ico)', tornado.web.StaticFileHandler, {'path': favicon_path})]
		]

		self.app = tornado.web.Application(handlers, **settings)
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
