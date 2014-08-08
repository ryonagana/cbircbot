#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from minicbircbot.packages.irc import ircClient


import logging



# logging
logging.basicConfig(filename='cbircbot.log', level=logging.INFO)
logger = logging.getLogger(__name__)


def init_bot():
	irc = ircClient()
	irc.connect()
	irc.auth()


	while irc.isRunning:



			
		try:
			data = irc.receiveData()
			irc.isServerRunning(data)
			print (data)
		except (KeyboardInterrupt):
			irc.exit_gracefully()

	