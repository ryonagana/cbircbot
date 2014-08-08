#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import logging
import re

from minicbircbot.packages.config.config_json import ConfigJson
from minicbircbot.packages.sockets.sockethandler import IrcSocket
from minicbircbot.utils import format, clean_str
from minicbircbot.packages.irc.irceventhandler import IrcEventhandler, IrcMessage, IrcPrivateMessage

logger = logging.getLogger(__name__)



class ircClient:

	def __init__(self):
		self.config = ConfigJson("config.json")
		self.config.load()
		self.ircsocket = IrcSocket(self.config.get("address") , self.config.get("port"))

		self.isRunning = False
		self.isJoined = False


		if self.config.get("console"):
			self.Console = IrcConsoleCommands(self)
		

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

		msg = data.decode('utf8')

		if msg.find('396') != -1:
			return True
		return False

	def receiveData(self):

		data = self.ircsocket.recv(4096);
		return data

	def receiveAsString(self):

		data = receiveData()
		return data.decode("utf-8")


	def PingPong(self, message):

		msg = message.decode("utf-8")
		if msg.find("PING") != -1:
			print ("SERVER: PING!")
			self.ircSend("PONG {0}".format(message.split()[1]))
			print("CLIENT: PONG!")



	def ircEventHandler(self, data):

		self.PingPong(data)
		if self.detectEndMOTD(data):
			if not self.isJoined:
				self.JoinChannels(self.config.get("chans"))
				self.isJoined = True
				
				if self.config.get("console"):
					self.Console.start()

		self.parseServerData(data)




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


	def parseServerData(self, message):
		
		server_msg = clean_str(message.decode("utf-8"))


		
		if server_msg.find("PRIVMSG") != -1:
			is_message  = re.search("^:(.+[aA-zZ0-0])!(.*) PRIVMSG (.+?) :(.+[aA-zZ0-9])$", server_msg)

			if is_message:

				data = {

					'sender'    : is_message.groups()[0], #sender's nickname
					'ident'		: is_message.groups()[1], #ident
					'channel'   : is_message.groups()[2], #channel
					'message'   : is_message.groups()[3], #message
				}
				
				if data['channel'].startswith("#") == -1:
					message_received = IrcPrivateMessage.register(data)
				else:
					message_received = IrcMessage.register(data)

				self.ReceivedMessages(message_received)
		
				


		


	def ReceivedMessages(self, msg):
		print(msg)












