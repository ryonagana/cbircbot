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
		self.owner = "" #owner of the bot  if you want to retrict a command being run by only one person
		self.version = "" #version
		self.author = "" #author name
		self.permissions = BOT_RUN_ALL # permissions
		self.reg_command = {}
		


	def args(self, args):
		
		prefix = args[:1]
		command = args[1:].split(' ')

		return (prefix, command)
		#return args.split()

	def isCommand(self,msg, prefix):
		cmd = msg.split()
		if cmd[0].startswith(prefix):
			return True
		return False

	def register_command(self, command, func_callback):

		if command and func_callback:
			prefix = command[:1]
			cmd = command[1:]
			self.reg_command[cmd] = (prefix, func_callback)

	def exec_cmd(self,command, irchandler, *args, **kwargs):
		cmd = command[0]
		self.reg_command[cmd][1](irchandler)


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

