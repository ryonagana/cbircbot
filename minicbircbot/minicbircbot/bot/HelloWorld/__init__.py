import datetime


from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface


class HelloWorld(IrcBotInterface):
	def __init__(self, irc = None):
		super().__init__(irc)


		self.owner = ["seunick"]
		
		self.module_name = "HelloWorld"

		#registra o comando no modulo onde vai ser gerado o help automaticamente
		#basta ir no PVT do bot e digitar !help HelloWorld
		#e vai mostrar a lista de comandos registrados

		
		#comando !hello do tipo somente PVT 
		self.register_command("!hello", self.doHelloWorld,  self.CMD_TYPE_BOTH, "my description")


	def doHelloWorld(self, handler):

		irc, msghandler = handler # captura 2 handlers que são repassado para todos os modulos
		prefix, command, count = self.args(msghandler.message) #verifica as funções e retorna separadadas
		#prefix é caracter de comando (neste caso  o !)
		#command é o texto do comando que voce digitou no caso ela pertence ao !hello então retorna "hello" sem o !
		#count retorna a quantidade de parametros sem contar  o comando para ter controle

		#irc e a referencia a classe principal do irc
		#msghandler retorna informações da pessoa que ativou o comando
		chans = irc.config.get("chans") #pega os canais que voce definiu no config.json 

		irc.ircSendMessage(chans, "hello world!")






