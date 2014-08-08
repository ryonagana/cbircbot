#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import logging

from minicbircbot.packages.config.config_json import ConfigJson
from minicbircbot.packages.sockets.sockethandler import IrcSocket
from minicbircbot.utils import format


logger = logging.getLogger(__name__)


class ircClient:

	def __init__(self):
		self.config = ConfigJson("config.json")
		self.config.load()
		self.ircsocket = IrcSocket(self.config.get("address") , self.config.get("port"))

		self.isRunning = False
		self.isJoined = False
		

		#teste
		#self.sock = socketserver.TCPServer( ("localhost", 9999), MainLoop) 

	#def ServerMessages(self, data):


	def auth(self):
			self.ircSend("NICK {0}".format(self.config.get("nickname")))
			self.ircSend("USER {0} {1} {2} :{3}".format( self.config.get("nickname"), self.config.get("address"), self.config.get("identd"), 'Test'))
			logger.info("Auth Sent")
	def connect(self):

		if self.ircsocket.createConnection():
			self.isRunning = True
			logger.info("Connected Successfully!")

	def ircSend(self, message):
		self.ircsocket.send(format(message))

	def ircJoin(self, channel):
		if type(channel) == str:

			if( channel.startswith("#") != -1):
				self.ircSend("JOIN {0}".format(channel))
			else:
				self.ircSend("JOIN #{0}".format(channel))
			

	def JoinChannels(self, channels):

		if type(channels) is (dict, list):
				for c in channels:
					self.ircJoin(c)

		elif type(channels) is str:
			self.ircJoin(channels)

			


	def detectEndMOTD(self, data):
		if data.find('396') != -1:
			return True
		return False

	def receiveData(self):
		return self.ircsocket.recv(4096);

	def PingPong(self, message):
		if message.find("PING") != -1:
			print ("SERVER: PING!")
			self.ircSend("PONG {0}".format(message.split()[1]))
			print("CLIENT: PONG!")



	def ircEventHandler(self, data):

		self.PingPong(data)

		if self.detectEndMOTD(data):
			if not self.isJoined:
				self.JoinChannels(self.config.get("chans"))
				self.isJoined = True




	def isServerRunning(self, data):

		if not self.isRunning:	
			return False
		

		self.ircEventHandler(data)
		return True

	def exit_gracefully(self):
		self.isRunning = False
		time.sleep(1)
		self.ircsocket.force_close()
		logger.info("Socket Closed With Success!")











