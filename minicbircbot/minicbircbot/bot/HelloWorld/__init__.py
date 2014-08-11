from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface


class HelloWorld(IrcBotInterface):
	def __init__(self):
		super().__init__()
		self.register_command("!hello", self.doHelloWorld )
		
	def onReceivedChannelMessage(self, irchandler, messagehandler):
		
		args = self.args(messagehandler.message)
		prefix = args[0]
		command = args[1]
		count = len(args[1])

	

		if count == 1:
			#if  self.isCommand(args[1],args[0]):
			self.exec_cmd(args[1], irchandler)



		#irchandler.ircSendMessage("#python", "message in Channel")

	def onReceivedPrivateMessage(self, irchandler, messagehandler):
		irchandler.ircSendMessage("#python", "HelloWorld!!! from Plugin")


	def doHelloWorld(self, irchandler):
		irchandler.ircSendMessage("#python", "Hello World Via Command")