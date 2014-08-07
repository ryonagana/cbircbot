# -*- coding: utf-8 -*-
import os
import sys
import socketserver
import threading
import logging


logger = logging.getLogger(__name__)




class SocketHandler(socketserver.BaseRequestHandler):



	def handle(self):
		self.data = self.request.recv(4096)
		print (self.data)






class TCPServerThread(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass