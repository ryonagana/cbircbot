# -*- coding: utf-8 -*-

class IrcCommand(object):
	""" simple class to hold command data easily """

	#better than using dictionaries which every update
	#you need to change  many things
	#and  when you update the class you just add new things
	#the objects remains the same


	prefix = ""
	cmd_name = ""
	func_callback = ""
	cmd_description = ""
	access = 6


	def __init__(self):
		pass


	def load(self, **data):

		if "prefix" in data:
			self.prefix = data['prefix']


		if "cmd_name" in data:
			self.cmd_name = data['cmd_name']


		if "func_callback" in data:
			self.func_callback = data['func_callback']

		
		if "cmd_description" in data:
			self.cmd_description = data["cmd_description"]


		if "access" in data:
			self.access = data["access"]



	def run(self, handlers):

		if self.func_callback:
			self.func_callback(handlers)





