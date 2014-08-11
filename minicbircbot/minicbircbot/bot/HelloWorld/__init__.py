import datetime


from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface


class HelloWorld(IrcBotInterface):
	def __init__(self):
		super().__init__()
		self.register_command("!hello", self.doHelloWorld )
		self.register_command("!time", self.showTime)
		
	def onReceivedChannelMessage(self, irchandler, messagehandler):
		
		prefix, command  = self.args(messagehandler.message)

		count = len(command)


		self.exec_cmd(command[0], (irchandler, messagehandler) )



		#irchandler.ircSendMessage("#python", "message in Channel")

	def onReceivedPrivateMessage(self, irchandler, messagehandler):
		irchandler.ircSendMessage("#python", "HelloWorld!!! from Plugin")


	def doHelloWorld(self, handlers):

		irc, msg = handlers
		prefix, command = self.args(msg.message)
		c = len(command)

		if(c != 1):
			irc.ircSendMessage(msg.receiver, "Invalid Parameters")
		else:
			irc.ircSendMessage("#python", "Hello World Via Command")
		

	def showTime(self, handlers):

		irc, msg = handlers
		prefix, command = self.args(msg.message)
		c = len(command)

		if c == 2:
			if( command[1].find("now") != -1):
				d = "Today is: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
				irc.ircSendMessage(msg.receiver, d)
			else:
				irc.ircSendMessage(msg.receiver, "BEEEEP: Wrong Answer!")

		else:
			irc.ircSendMessage(msg.receiver, "whatchu talkin' bout willis?")





