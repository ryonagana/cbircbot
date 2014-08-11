#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import logging
import re
import importlib



from minicbircbot.packages.config.config_json import ConfigJson
from minicbircbot.packages.sockets.sockethandler import IrcSocket
from minicbircbot.utils import format, clean_str, DEBUG_MODE, MODULES_LOADED
from minicbircbot.packages.irc.irceventhandler import IrcEventhandler, IrcMessage, IrcPrivateMessage
import minicbircbot.bot

logger = logging.getLogger(__name__)



class ircClient:

	def __init__(self):
		self.config = ConfigJson("config.json")
		self.config.load()
		self.initModules()

		if DEBUG_MODE:
			print("Loading Modules: ")
			print(self.config.get("modules"))
			print (MODULES_LOADED)
			print("------------------------")

		self.ircsocket = IrcSocket(self.config.get("address") , self.config.get("port"))

		self.isRunning = False
		self.isJoined = False


		if self.config.get("console"):
			self.Console = IrcConsoleCommands(self)
		

		#teste
		#self.sock = socketserver.TCPServer( ("localhost", 9999), MainLoop) 

	#def ServerMessages(self, data):


	def initModules(self):
		global MODULES_LOADED
		
		for mod in self.config.get("modules"):
			#Who's bad?

			#i'm so evil that i'm using eval
			#the devil of programming 
			# >=)
			try:
				module_loaded = self.instantiateModule(mod)
				MODULES_LOADED[mod] = module_loaded()


			except Exception as ex:
				print(ex)
				#print("-------------------------------------------------")
				#print("MODULE \"{0}\" doesnt exists. and will be ignored".format(mod))
				#print("-------------------------------------------------")
				#print("")
				continue
			
		print ("Instance -------------------------------------------:")
		print (MODULES_LOADED)
		print ("-----------------------------------------------------")



	def instantiateModule(self, module_name):

		namespace = "minicbircbot.bot."
		inst = None
		module = None

		try:
			inst =  __import__(namespace + module_name, fromlist=module_name) #importlib.import_module(namespace + module_name, module_name)
			return getattr(inst, module_name)
		
		except Exception as ex:
			print("ERROR: Cannot Instantiate {0}".format(module))
			print("Exception: {0}".format(str(ex)))
			return inst






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


	def ircSendMessageTo(self, sender, receiver, message):
		self.ircSend("PRIVMSG {0} :{1}".format(receiver, message ))


	def ircSendMessage(self, channel, message):
		self.ircSend("PRIVMSG {0} :{1}".format(channel, message))



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
					'receiver'   : is_message.groups()[2], #channel or receiver's nickname
					'message'   : is_message.groups()[3], #message
				}

				print ('DATA DEBUG: ')
				print(data)
				

				
				if data['receiver'].startswith("#"): 
				
					#means you are sending message directly to a channel
					message_received = IrcMessage.register(**data)
					self.ReceivedMessageChannel(message_received)
				else:
					
					#means you are sending message directly to someone
					message_received = IrcPrivateMessage.register(**data)
					self.ReceivedPrivateMessages(message_received)
					

				


		print(server_msg)
		
				


		


	def ReceivedMessageChannel(self, msghandler):
		
		for mod in MODULES_LOADED:
			if MODULES_LOADED[mod]:
				MODULES_LOADED[mod].onReceivedChannelMessage(self,msghandler)
		#print(msghandler)onReceivedChannelMessage

	def ReceivedPrivateMessages(self, msghandler):

		#print("DEBUG HelloWorld")
		#print( dir(MODULES_LOADED['HelloWorld']))
		
		
		for mod in MODULES_LOADED:
			if MODULES_LOADED[mod]:
				MODULES_LOADED[mod].onReceivedPrivateMessage(self,msghandler)
		












