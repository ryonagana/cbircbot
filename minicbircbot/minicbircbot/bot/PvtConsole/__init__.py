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
		
		self.module_name = "PvtConsole"

		self.register_command("!say", self.sayToChannel, self.CMD_TYPE_PVT, "say something in the channel")
		self.register_command("!reload", self.reloadModules, self.CMD_TYPE_PVT, "reload all  external modules")
		self.register_command("!op", self.giveOp, self.CMD_TYPE_BOTH, "give op")
		self.register_command("!disconnect", self.disconnectBot, self.CMD_TYPE_PVT, "get of a channel")
		self.register_command("!join", self.joinBot, self.CMD_TYPE_PVT, "enters in a channel")


	def onChannelJoined(self, irchandler, messagehandler):
		super().onChannelJoined(irchandler, messagehandler)
		

		#example of greeting
		irchandler.ircSendMessage(messagehandler.channel_joined, "Oi {0} Seja Bem Vindo ao {1}".format(messagehandler.sender, messagehandler.channel_joined ) )


	def onChannelPart(self, irchandler, messagehandler):
		super().onChannelPart(irchandler, messagehandler)
		print("SAIU")
		
	def onReceivedPrivateMessage(self, irchandler, messagehandler):
		super().onReceivedPrivateMessage(irchandler, messagehandler)

		
	def onReceivedChannelMessage(self, irchandler, messagehandler):
		super().onReceivedChannelMessage(irchandler, messagehandler)


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


	def disconnectBot(self, handlers):



		irc, msghandler = handlers
		prefix, command, count = self.CMD_Args(msghandler.message)

		chans = irc.config.get("chans")


		if count == 1 and command[1] == "all" and msghandler.sender in self.owner  :
			if type(chans) is (list, tuple):

				for c in chans:
					irc.ircDisconnect(c)
					print("Part {0}".format(c))
					irc.ircSendMessage(msghandler.sender, "Disconnected from {0} with success".format(c))


			if type(chans) is str:
				irc.ircDisconnect(chans)
				print("Part {0}".format(chans))
				irc.ircSendMessage(msghandler.sender, "Disconnected from {0} with success".format(chans))
		else:
			return
			#irc.ircSendMessage(msghandler.sender, "[Command Failed]")


	def joinBot(self, handlers):

		irc, msghandler = handlers
		prefix, command, count = self.CMD_Args(msghandler.message)

		chans = irc.config.get("chans")

		if count == 1 and command[1].find("#") != -1 and msghandler.sender in self.owner:
			irc.JoinChannels(chans)