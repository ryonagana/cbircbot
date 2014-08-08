#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys


class IrcEventhandler:

	sender = ""
	receiver = ""
	channel = ""
	message = ""

	def __init__(self):
		pass

	@staticmethod
	def register(self, sender, receiver, channel,  message):
		event = IrcEventhandler()


		event.sender = sender
		event.receiver = receiver
		event.channel = channel
		event.message  = message

		return event