# -*- coding: utf-8 -*-

import os
import sys


#run permissions
BOT_RUN_NONE = 1
BOT_RUN_USER = 2
BOT_RUN_VOICE = 4
BOT_RUN_OP = 8 
BOT_RUN_ALL = 16


class IrcBotInterface:


	def __init__(self):
		self.owner = "" #owner of the bot  if you want to retrict a command run by only one person
		self.version = "" #version
		self.author = "" #author name
		self.permissions = BOT_RUN_ALL # permissions
		


	def args(self, args):
		return args.split()


	def onReceivedPrivateMessage(self, irchandler, messagehandler):
		pass

	def onReceivedChannelMessage(self, irchandler, messagehandler):
		pass

	def onPart(self, irchandler, messagehandler):
		pass

	def onJoined(self, irchandler, messagehandler):
		pass

	def onNickChanged(self, irchandler, messagehandler):
		pass

