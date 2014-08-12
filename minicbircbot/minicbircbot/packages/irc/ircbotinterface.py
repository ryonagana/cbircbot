# -*- coding: utf-8 -*-
import sphinx.ext.autodoc
import os
import sys
from minicbircbot.utils import MODULES_LOADED

"""
This Class is an Abstract Class to make all modules with the  same class signature


"""


#run permissions
BOT_RUN_NONE = 1
BOT_RUN_USER = 2
BOT_RUN_VOICE = 4
BOT_RUN_OP = 8 
BOT_RUN_ALL = 16




__author__ = "Nicholas Oliveira <ryonagana@gmail.com>"
__date__ = "12 August 2014"

__version__ = "$Revision: 88564 $"
__credits__ = """Guido van Rossum, for an excellent programming language.
				 Jerónimo Barraco Marmól,  being  excellent programmer, gamer and friend.
"""


class IrcBotInterface:


	def __init__(self):
		self.owner = "" #owner of the bot  if you want to retrict a command being run by only one person
		self.version = "" #version
		self.author = "" #author name
		self.permissions = BOT_RUN_ALL # permissions
		self.reg_command = {}
		


	def args(self, args):
		""" gets the irc message  and split into  command and arguments """
		prefix = args[:1]
		command = args[1:].split(' ')

		return (prefix, command)
		#return args.split()

	def  getMessageArgs(self, args):
		""" same of args with better name  cause args is too generic and clunky name """
		return self.args(args)

	def isCommand(self,msg, prefix):
		""" Check is message is a command """
		cmd = msg.split()
		if cmd[0].startswith(prefix):
			return True
		return False

		

	def register_command(self, command, func_callback):
		""" Register new command in the module
			All commands names mus be unique. im trying to figure how to not conflict names
	    """




		if command and func_callback:


			prefix = command[:1]
			cmd = command[1:]

			self.reg_command[cmd] = (prefix, func_callback)

	def exec_cmd(self,command, handlers, *args, **kwargs):
		""" execute  the command when called  it doesnt run in array
			if the right name is passed  they just call once.

		"""
		if command in self.reg_command:
			self.reg_command[command][1](handlers)


	def onReceivedPrivateMessage(self, irchandler, messagehandler):
		""" abstract method when  the bot receives a private message """
		pass

	def onReceivedChannelMessage(self, irchandler, messagehandler):
		""" abstract method when  the bot receives message in channel
			it captures all messages in channel no exceptions.  you must program the module
			how to filter  the content in the channel
		"""
		pass

	def onPart(self, irchandler, messagehandler):
		"""
		abstract method when someone parts the channel trigger  this event
		"""
		pass

	def onJoined(self, irchandler, messagehandler):
		"""
		abstract method when someone join the channel   this event is triggered
		"""
		pass

	def onNickChanged(self, irchandler, messagehandler):
		""" 
		when someone changes the nick in the channel the bot triggers this event
		"""
		pass

