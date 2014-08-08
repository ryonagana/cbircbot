# -*- coding: utf-8 -*-
import os
import sys
import socket
import logging
import time
from minicbircbot.utils import format


logger = logging.getLogger(__name__)




class IrcSocket:

	def __init__(self, host, port):
		self.host = host
		self.port = int(port)

		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)


	def createConnection(self):
		try:
			self.sock.connect_ex( (self.host, self.port) )
			return True;
		except:
			return False
		return
		
	def send(self, message):
		self.sock.send( bytes(format(message), "utf-8") )
		return

	def recv(self, size):

		if type(size) == int:
			data =	self.sock.recv(size)
			return str(data)
		else:
			raise Exception("Error")

	def force_close(self):
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()

	def exit_gracefully(self):
		time.sleep(1)
		self.force_close()


