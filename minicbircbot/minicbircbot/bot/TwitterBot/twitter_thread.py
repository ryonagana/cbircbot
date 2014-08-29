import threading
from threading import Thread
import random

class TwitterService(Thread):

	def __init__(self, api, irc, search, count, *args, **kwargs):

		super().__init__()

		self.twitter = api
		self.irc = irc
		self.search = search
		self.count = count


	def run(self):

		irc = self.irc['irc']
		msg = self.irc['messagehandler']
		irc.ircSendMessage(msg.receiver, "Fetching Tweets. it will take some time..  Take a break")

		data = self.twitter.search(self.search, self.count) 
		

		for item in data:
			print (item)


		#lucky  = random.choice(data)
		#irc.ircSendMessage(msg.receiver, lucky['text'])








