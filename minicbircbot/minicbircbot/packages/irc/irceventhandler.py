#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
import copy


class IrcEventhandler:

	events = {
		'sender'   : '',
		'ident'	   : '',
		'channel'  : '',
		'receiver' : '',

	}

	def __init__(self):
		pass

	def __str__(self):

		s = ""

		for name,val in self.events.items():
			s += "{0}: {1}\n".format(name, val)
		
		return s



	def __repr__(self):

		for name,val in self.events.items():
			print("{0}: {1}".format(name, val))


	@staticmethod
	def register(self, *args, **kwargs):
		event = IrcEventhandler()

		for k,v in kwargs.items():
			event.events[k] = v

		return event



class IrcMessage(IrcEventhandler):



	def __init__(self):

		self.events['message'] = ''
		super().__init__()



class IrcPrivateMessage(IrcMessage):

	def __init__(self):
		self.events['pvt'] = ''
		super().__init__()