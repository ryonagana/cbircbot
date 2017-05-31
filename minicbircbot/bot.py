#!/usr/bin/env python3
import os
import sys
import importlib

import minicbircbot
import minicbircbot.utils

def check_root():
	try:
		if (os.getuid() == 0 or os.geteuid() == 0 or os.seteuid(0)):
			print("Dont Run as Root! privileges")
			sys.exit(0)
		return True
	except AttributeError:
		pass



if __name__ == "__main__":
	check_root()
	minicbircbot.utils.load_extra_paths()
	minicbircbot.motd()
	minicbircbot.init_bot()
