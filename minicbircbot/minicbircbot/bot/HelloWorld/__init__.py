from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface


class HelloWorld(IrcBotInterface):
	def __init__(self):
		super().__init__()
		

	def onReceivedPrivateMessage(self, irchandler, messagehandler):
		irchandler.ircSendMessage("#python", "HelloWorld!!! from Plugin")