#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from minicbircbot.packages.irc import ircClient


import logging
import colorama
from colorama import Fore, Back, Style


# logging
logging.basicConfig(filename='cbircbot.log', level=logging.INFO)
logger = logging.getLogger(__name__)


def init_bot():
	colorama.init()
	


	irc = ircClient()
	
	if not irc.isConnected:
		irc.connect()
		irc.auth()
	

	while irc.isRunning:



			
		try:
			data = irc.receiveData()
			irc.isServerRunning(data)
			#print (data)
		except (KeyboardInterrupt):
			print(Fore.YELLOW + "Waiting 2 seconds")
			print(Fore.RED + "Closing Sockets")
			logger.info("Desconnecting Socket")
			irc.exit_gracefully()
			logger.info("Successfully Closed")


