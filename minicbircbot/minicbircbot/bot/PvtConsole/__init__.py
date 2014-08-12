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

		self.owner = ["vagrant", "ryonagana"]
		self.register_command("!say", self.sayToChannel, self.CMD_TYPE_PVT)
		self.register_command("!reload", self.reloadModules, self.CMD_TYPE_PVT)
		self.register_command("!op", self.giveOp, self.CMD_TYPE_BOTH)



	def onReceivedPrivateMessage(self, irchandler, messagehandler):
		super().onReceivedPrivateMessage(irchandler, messagehandler)

		


	def onReceivedChannelMessage(self, irchandler, messagehandler):
		super().onReceivedChannelMessage(irchandler, messagehandler)


	def usage(self, irchandler, msghandler):
		
		s = "!say #channel message"
		irchandler.ircSendMessageTo(msghandler.receiver, s)
		time.sleep(500)
		s = "!say message"
		irchandler.ircSendMessageTo(msghandler.receiver, s)
		time.sleep(500)
		s = " will send to all channels"
		irchandler.ircSendMessageTo(msghandler.receiver, s)




	def giveOp(self, handlers):
		irc, msghandler = handlers
		prefix, cmd, count_args = self.getMessageArgs(msghandler.message)
		

		
		if count_args >= 2:
			irc.ircSetMode(cmd[1], "o", *cmd[2:])
	
		#if not msghandler.sender in self.owner:
		#	irc.ircSendMessageTo(msghandler.sender, "[Denied]")

		#irc.ircSetMode(cmd[1], "o", cmd[2] )








		
	def reloadModules(self, handlers):
		

		irc, msghandler = handlers

		prefix, cmd, c = self.args(msghandler.message)


		if  c == 1 and msghandler.sender in self.owner:
			chans = irc.config.get("chans")
			#this doesnt work :( modules still the same  i just want to reload them runtime but nothing happens
			#FIX ME
			irc.initModules()
			print(cons.TESTE)
			irc.ircSendMessage(chans, "::Reloading Matrix Proudly Running in Win95:: ")



	def sayToChannel(self, handlers):

		irc, msghandler = handlers
		prefix, command, count = self.args(msghandler.message)


		
		if not msghandler.sender in self.owner:
			print("SENDER: {0}".format(msghandler.sender) )
			irc.ircSendMessageTo(msghandler.sender, "you are not my owner!")
			return
		
		#avoid split spaces in the messages
		channel = command[1]
		msg =  str(" ".join(command[2:]))
		irc.ircSendMessage(channel, msg)
			
		#print(prefix, msg)