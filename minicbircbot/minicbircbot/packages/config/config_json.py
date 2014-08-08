# -*- coding: utf-8 -*-
import os
import sys
import json
import copy, base64
from base64 import b64encode, b64decode
from copy import copy
from  io import StringIO
import logging
import zlib

logger = logging.getLogger(__name__)



#yes overhead everywere but i dont care. it just load  small pieces of code
#nothing important  impact is almost zero. uncompressing a zip has  more overhead than this code
#kthx bye


class ConfigJson(object):

	DEFAULT_OPTS = {

					'address' : 'irc.falai.org',
					'port' : 6667,
					'chans': '#python',
					'nickname' : 'mrTest',
					'identd' : 'HUE',

					'modules' : {}
					

					}


	def __init__(self,cfg, use_base64 = True):
		self.cfg_path = cfg
		self.opts = {}
		self.usebase64  = use_base64

	
	def encode(self,str):
		return b64encode(str)

	def decode(self, str):
		return b64decode(str)

	def load(self):
		logging.info("Tried to load CFG")
		try:
			with open(self.cfg_path, mode="r", encoding="utf-8") as f:
				


				cfg = json.load(f)

	
				self.opts = copy(cfg)
				#logger.warning("READING:  {0}".format(self.opts) )

		except Exception as ex:
				
				
				with open(self.cfg_path, mode="w", encoding="utf-8") as f:
						
						default_opts = copy(self.DEFAULT_OPTS)


						json.dump(default_opts, f, indent=4, sort_keys=True)
						#self.opts.clear()
						self.opts = copy(default_opts)
						#logger.warning("WRITING:  {0}".format(data) )
					
						

	def save(self):

		with open(self.cfg_path, mode="w", encoding="utf-8") as f:



			json.dump(self.opts, f, indent=4, sort_keys=True)
			


	
	def edit(self, key, value):
		if not key and not value:
			return

		try:
			self.opts[key] = value
		except:
			logger.warning("{0} : Nao Existe".format(key))

			#print ("{0} : Nao Existe".format(key))

	def get(self, key):

			try:
				return self.opts[key]
			except Exception as msg:
				logger.warning("config: get():|    Chave: {0} Nao Encontrada".format(key))
				#print ("config: get():|    Chave: {0} Nao Encontrada".format(key))