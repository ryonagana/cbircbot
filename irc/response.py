# -*- coding: utf-8 -*- 
import os
import sys


class Response:

	def __init__(self, filename):
		
		#self.fp 

		self.question = []
		self.answer = []
		
		try:
			with(open(filename, "rb")) as fp:
				self.processLines(fp)

		except Exception, error:
			print error

	


	def processLines(self, fileobject):

		for line in fileobject.readlines():
			linestripped = line.replace('\r\n','')

			if linestripped.startswith(">"):
				self.question.append(linestripped.replace(">",''))
			
			elif linestripped.startswith("-"):
				self.answer.append(linestripped.replace("-",''))
