import os
import sys

from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface
import configparser

class AutoResponse(IrcBotInterface):


	def __init__(self, irc = None):
		super().__init__(irc)

		c = configparser.ConfigParser()
		f = None

		c['TALK'] = {
			'hi' : 'hello',
			'how r*' : 'i am fine thanks!',
			'asl' : '18/f/usa',
		}


		if not os.path.isfile("talk.txt"):
			f = open("talk.txt", "w")
			c.write(f)
		else:
			f = open("talk.txt", "r")
			c.read(f)

		f.close()






	def onReceivedChannelMessage(self, irchandler, messagehandler):
		super().onReceivedChannelMessage(irchandler, messagehandler)
