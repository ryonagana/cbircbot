#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import time
import logging
import re
import importlib
import sphinx.ext.autodoc

"""
This Class has all irc handlers  and is intended  to create methods for IRC only


"""

__author__ = "Nicholas Oliveira <ryonagana@gmail.com>"
__date__ = "12 August 2014"

__version__ = "$Revision: 88564 $"
__credits__ = """Guido van Rossum, for an excellent programming language.
				 Jerónimo Barraco Marmól,  being  excellent programmer, gamer and friend.
"""





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
		""" init all modules you wrote in config.json
			search in minicbircbot.bot.* for modules
			and create a new instance in the global variable
			MODULES_LOADED
		"""
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
				
				print("-------------------------------------------------")
				print("MODULE \"{0}\" doesnt exists. and will be ignored".format(mod))
				print("Exception: {0}".format(ex))
				print("-------------------------------------------------")
				print("")
				
				continue
			
		print ("Instance -------------------------------------------:")
		print (MODULES_LOADED)
		print ("-----------------------------------------------------")



	def instantiateModule(self, module_name):
		"""  
			when the module is in memory it tried to create a new instance of the module 
			returns the module object - ircBotInterface child class
		"""
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
			""" make the irc auth sending your credentials"""
			self.ircSend("NICK {0}".format(self.config.get("nickname")))
			self.ircSend("USER {0} {1} {2} :{3}".format( self.config.get("nickname"), self.config.get("address"), self.config.get("identd"), 'Test'))
			logger.info("Auth Sent")


	def connect(self):
		""" create a new socket  and try to connect  the server """
		if self.ircsocket.createConnection():
			self.isRunning = True
			logger.info("Connected Successfully!")

	def ircSend(self, message):
		""" Send a Simple message to server """
		self.ircsocket.send(format(message))


	def ircSendMessageTo(self, receiver, message):
		""" intended only to send direct messages to someone (pvt messages) """
		if not receiver.startswith("#"):
			self.ircSend("PRIVMSG {0} :{1}".format(receiver, message ))

	def ircSendMessageQuote(self, sender, receiver,  message ):
		""" Sends a message to the channel call the name of the receiver """
		if not sender or not message:
			return

		self.ircSend("PRIVMSG {0} :{1}".format(

												receiver,
												"{0}: {1}".format(sender, message)
			))


	def ircSendMessage(self, channel, message):
		""" send a message directly to a channel """
		self.ircSend("PRIVMSG {0} :{1}".format(channel, message))



	def ircJoin(self, channel):
		""" join the bot in a channel """
		if type(channel) == str:

			if( channel.startswith("#") != -1):
				self.ircSend("JOIN {0}".format(channel))
			else:
				self.ircSend("JOIN #{0}".format(channel))


			

	def JoinChannels(self, channels):
		""" join the bot in all channels in config.json  if just a simple string make a join, if channels is  a list 
			make a simple join loop - obs this function  can only being called when  end of MOTD is detected
		"""

		if type(channels) is (dict, list):
				for c in channels:
					self.ircJoin(c)

		elif type(channels) is str:
			self.ircJoin(channels)

			


	def detectEndMOTD(self, data):
		""" detects when motd is finished to show, can vary server for server """
		msg = data.decode('utf8')

		if msg.find('396') != -1:
			return True
		return False

	def receiveData(self):
		""" method to receive 4 bytes """
		data = self.ircsocket.recv(4096);
		return data

	def receiveAsString(self):
		""" method convert  bytes to unicode """
		data = receiveData()
		return data.decode("utf-8")


	def PingPong(self, message):
		""" method when servers send a ping the bot responds with PONG """
		msg = message.decode("utf-8")
		if msg.find("PING") != -1:
			print ("SERVER: PING!")
			self.ircSend("PONG {0}".format(message.split()[1]))
			print("CLIENT: PONG!")



	def ircEventHandler(self, data):
		""" this method is  the heart of the bot 
			make all calling  trigger events repass data to parse
			to trigger bots events
		"""

		self.PingPong(data)
		if self.detectEndMOTD(data):
			if not self.isJoined:
				self.JoinChannels(self.config.get("chans"))
				self.isJoined = True
				
				if self.config.get("console"):
					self.Console.start()

		self.parseServerData(data)




	def isServerRunning(self, data):
		""" check if mainloop still running """
		if not self.isRunning:	
			return False
		

		self.ircEventHandler(data)
		return True

	def exit_gracefully(self):
		"""
			this method just make sure will not corrupt socket file descriptor
			just  end the main loop
			wait one second to socket  finish and close createConnection

		"""
		self.isRunning = False
		time.sleep(1)
		self.ircsocket.force_close()
		logger.info("Socket Closed With Success!")


	def parseServerData(self, message):
		"""
			this method generates  the events for the bot and trigger them in all external modules
		"""
		 # decode the message to utf8, sanitize the string removing '\r\n' or the regex will fail so badly
		server_msg = clean_str(message.decode("utf-8")) 


		#before make a check we must have sure is a message
		#PRIVMSG stand for 2 kinds of message, send to other person, or  regular message in the channel
		#the difference is the receiver

		if server_msg.find("PRIVMSG") != -1:  #is a message?

			is_message  = re.search("^:(.+[aA-zZ0-0])!(.*) PRIVMSG (.+?) :(.+[aA-zZ0-9])$", server_msg) # strip all contents useful for me

			if is_message:  #regex is successfull


				data = {

					'sender'    : is_message.groups()[0], #sender's nickname
					'ident'		: is_message.groups()[1], #ident
					'receiver'   : is_message.groups()[2], #channel or receiver's nickname
					'message'   : is_message.groups()[3], #message
				}

				if DEBUG_MODE:
					print ('DATA DEBUG: ')
					print(data)
				

				#if the receiver is a channel  trigger self.ReceivedMessageChannel, otherwise trigger self.ReceivedPrivateMessages
				if data['receiver'].startswith("#"): 
				
					#means you are sending message directly to a channel
					message_received = IrcMessage.register(**data)
					self.ReceivedMessageChannel(message_received)
				else:
					
					#means you are sending message directly to someone
					message_received = IrcPrivateMessage.register(**data)
					self.ReceivedPrivateMessages(message_received)
					

				


		print(server_msg)
		
				


		

	#send  event triggered to all modules loaded ReceivedMessageChannel
	def ReceivedMessageChannel(self, msghandler):
		
		
		for mod in MODULES_LOADED:
			if MODULES_LOADED[mod]:
				MODULES_LOADED[mod].onReceivedChannelMessage(self,msghandler)


	#send  event triggered to all modules loaded ReceivedPrivateMessages
	def ReceivedPrivateMessages(self, msghandler):


		
		for mod in MODULES_LOADED:
			if MODULES_LOADED[mod]:
				MODULES_LOADED[mod].onReceivedPrivateMessage(self,msghandler)
		












