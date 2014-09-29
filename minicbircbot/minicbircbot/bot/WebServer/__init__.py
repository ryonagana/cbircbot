import sys
import os


from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface
from minicbircbot.bot.WebServer.Server import Server


class WebServer(IrcBotInterface):
	def __init__(self, irc = None):
		super().__init__(irc)

		print("===================Starting webserver==============")
		self.server = Server(irc)
		self.server.start()




	def onReceivedChannelMessage(self, irchandler, messagehandler):
		super().onReceivedChannelMessage(irchandler, messagehandler)

		
		



	def destroyModule(self):
		print("Destroying Webserver")
		self.server.stop()
		#self.server.daemon = True





