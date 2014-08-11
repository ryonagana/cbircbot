import time
import sys
import os
import importlib


import minicbircbot.bot.PvtConsole.cons

from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface
from minicbircbot.utils import DEBUG_MODE, MODULES_LOADED

class PvtConsole(IrcBotInterface):

	def __init__(self):
		super().__init__()

		self.owner = ["vagrant"]
		self.register_command("!say", self.sayToChannel)
		self.register_command("!reload", self.reloadModules)


	def onReceivedPrivateMessage(self, irchandler, messagehandler):

		prefix, command  = self.args(messagehandler.message)
		self.exec_cmd(command[0], (irchandler, messagehandler) )


	def usage(self, irchandler, msghandler):
		
		s = "!say #channel message"
		irchandler.ircSendMessageTo(msghandler.receiver, s)
		time.sleep(500)
		s = "!say message"
		irchandler.ircSendMessageTo(msghandler.receiver, s)
		time.sleep(500)
		s = " will send to all channels"
		irchandler.ircSendMessageTo(msghandler.receiver, s)





		
	def reloadModules(self, handlers):
		

		irc, msghandler = handlers

		prefix, cmd = self.args(msghandler.message)


		if len(cmd) == 1 and msghandler.sender in self.owner:
			chans = irc.config.get("chans")
			#this doesnt work :( modules still the same  i just want to reload them runtime but nothing happens
			#FIX ME
			irc.initModules()
			print(cons.TESTE)
			irc.ircSendMessage(chans, "::Reloading Matrix Proudly Running in Win95:: ")



	def sayToChannel(self, handlers):

		irc, msghandler = handlers
		prefix, command = self.args(msghandler.message)


		
		if not msghandler.sender in self.owner:
			print("SENDER: {0}".format(msghandler.sender) )
			irc.ircSendMessageTo(msghandler.sender, "you are not my owner!")
			return
		
		#avoid split spaces in the messages
		channel = command[1]
		msg =  str(" ".join(command[2:]))
		irc.ircSendMessage(channel, msg)
			
		#print(prefix, msg)