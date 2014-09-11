#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import copy

"""
abstract class to pass the same handler to all events
"""


class IrcEventhandler:
	""" abstract class to pass all events with the same class signature  """
	
	

	sender = ""
	receiver = ""
	ident = ""
	message = ""

	def __init__(self, *args, **kwargs):

		if "sender" in kwargs:
			self.sender = kwargs['sender']
		if "receiver" in kwargs:
			self.receiver  = kwargs['receiver']
		if "ident" in kwargs:
			self.ident = kwargs['ident'] 
		if "message" in kwargs:
			self.message = kwargs['message']


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
		""" Register new command to a module """
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



class IrcMessageEvent(IrcEventhandler):

	""" Event Handler for All Messages """	



	def __init__(self):
		""" adds new attribute  message"""
		super().__init__()



class IrcPrivateMessageEvent(IrcMessageEvent):
	""" Event Handler for Private Messages """	
	receiver = ""

	def __init__(self):
		super().__init__()




class IrcJoinEvent(IrcEventhandler):

	channel_joined  = ""

	def __init__(self, **data):
		super().__init__(**data)
		self.channel_joined = data['channel_joined']







class IrcPartEvent(IrcEventhandler):

	quit_msg = ""
	channel_part = ""

	def __init__(self, **data):
		super().__init__(**data)

		self.quit_msg = data['quit_msg']
		self.channel_part = data['channel_part']