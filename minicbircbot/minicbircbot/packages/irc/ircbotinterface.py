# -*- coding: utf-8 -*-

import os
import sys

class IrcBotInterface:


	def __init__(self):
		pass
		


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

