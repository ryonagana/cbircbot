

import threading
import logging


from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface
from minicbircbot.bot.TwitterBot.twitter_calls import TwitterCalls
from minicbircbot.bot.TwitterBot.twitter_thread import TwitterService

logger = logging.getLogger(__name__)




class  TwitterBot ( IrcBotInterface ):

	def __init__(self, irc = None):
		super().__init__(irc)

		self.owner = ["ryonagana", "vagrant"]
		self.module_name = "TwitterBot"
		self.oauth_token= None
		self.oauth_secret = None
		self.consumer_key = None
		self.consumer_secret = None

		if irc:
			if not self.isAuth():

				""" Adds temporarily as  default config """


				self.oauth_token     =  self.irc.config.get("oauth_token")
				self.oauth_secret    =  self.irc.config.get("oauth_secret")
				self.consumer_key    =  self.irc.config.get("consumer_key")
				self.consumer_secret =  self.irc.config.get("consumer_secret")


				print("AUTH:")
				print(self.oauth_token)
				print(self.oauth_secret)
				print(self.consumer_key)
				print(self.consumer_secret)
				print ("END OF AUTH")


				try:
					self.api  = TwitterCalls(self.consumer_key, self.consumer_secret, self.oauth_token, self.oauth_secret)
				except Exception as ex:
					msg_ex = "TwitterAPI: EXCEPTION: " + str(ex)
					logger.critical(msg_ex)
					print (msg_ex)
		
			else:
				error_msg =  "Twitter is not logged it will ignore  all commands ultil you do login\n"
				error_msg += "please add this  keys in config.json:\n"
				error_msg += "oauth_token, oauth_secret, consumer_key, consumer_secret"
				logging.critical(error_msg)
				print (error_msg)

			
			


		

		self.register_command("!whatson", self.tweet_python, self.CMD_TYPE_BOTH, "Show Some Tweet from python")



	def isAuth(self):
		if self.oauth_token and self.oauth_secret and self.consumer_key and self.consumer_secret:
			return True

		return False




	def onChannelJoined(self, irchandler, messagehandler):
		super().onChannelJoined(irchandler, messagehandler)
		

	def onChannelPart(self, irchandler, messagehandler):
		super().onChannelPart(irchandler, messagehandler)
		print("SAIU")
		
	def onReceivedPrivateMessage(self, irchandler, messagehandler):
		super().onReceivedPrivateMessage(irchandler, messagehandler)

		
	def onReceivedChannelMessage(self, irchandler, messagehandler):
		super().onReceivedChannelMessage(irchandler, messagehandler)


	def tweet_python(self, handlers):

		if self.irc and self.isAuth():
			irc, msghandler = handlers
			prefix, cmd, count_args = self.getMessageArgs(msghandler.message)

			data = {
				'irc': irc,
				'messagehandler' : msghandler
			}


			service = TwitterService(self.api, data, '#python', 10)
			service.start()

		 #print service.result





