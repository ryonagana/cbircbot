from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface

class AutoResponse(IrcBotInterface):
	
	def __init__(self):
		super().__init__()

		self.register_command("!register", self.doRegister )



	def onReceivedChannelMessage(self, irchandler, messagehandler):

		prefix, command, count  = self.args(messagehandler.message)
		count = len(command)
		self.exec_cmd(command[0], (irchandler, messagehandler) )


	def doRegister(self, handlers):

		irc, msg, count = handlers
		prefix, command = self.args(msg.message)
		irc.ircSendMessage(msg.receiver, "Register From Auto Response")
