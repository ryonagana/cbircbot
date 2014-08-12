#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sphinx.ext.autodoc

import os
import sys
import copy

"""
abstract class to pass the same handler to all events
"""


class IrcEventhandler:

	sender = ""
	receiver = ""
	ident = ""
	message = ""

	def __init__(self):
		pass

	def __str__(self):
		s = ""
		s += "sender: {0}\n".format(self.sender)
		s += "receiver: {0}\n".format(self.receiver)
		s += "ident: {0}\n".format(self.ident)
		s += "message: {0}\n".format(self.message)

		return s

	def __repr__(self):
		print ("sender: {0}".format(self.sender))
		print ("receiver: {0}".format(self.receiver))
		print ("ident: {0}".format(self.ident))
		print ("message: {0}".format(self.message))


	@staticmethod
	def register(*args, **kwargs):
		event = IrcEventhandler()

		#print(kwargs)
		if "sender" in kwargs:
			event.sender = kwargs['sender']
		if "receiver" in kwargs:
			event.receiver  = kwargs['receiver']
		if "ident" in kwargs:
			event.ident = kwargs['ident'] 
		if "message" in kwargs:
			event.message = kwargs['message']


		return event



class IrcMessage(IrcEventhandler):




	def __init__(self):

		self.events['message'] = ''
		super().__init__()



class IrcPrivateMessage(IrcMessage):

	receiver = ""

	def __init__(self):
		super().__init__()