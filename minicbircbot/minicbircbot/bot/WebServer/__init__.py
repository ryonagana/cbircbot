import sys
import os


from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface
from minicbircbot.bot.WebServer.Server import Server


class WebServer(IrcBotInterface):
	def __init__(self, irc = None):
		super().__init__(irc)

		self.server = Server()
		self.server.initServer()
		self.server.run()
		#self.server.setDaemon(True)
		#self.server.start()





