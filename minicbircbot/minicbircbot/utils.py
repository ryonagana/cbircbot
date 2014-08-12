# -*- coding: utf-8 -*-

import os
import sys

#constants

if not'DEBUG_MODE' in globals():
	global DEBUG_MODE 
	DEBUG_MODE = False

if not 'MODULES_LOADED' in globals():
	global MODULES_LOADED
	MODULES_LOADED = {}

if not 'ROOT_PATH' in globals():
	global ROOT_PATH
	ROOT_PATH = os.getcwd()

if not 'BOT_PATH' in globals():
	global BOT_PATH
	BOT_PATH = os.path.join(ROOT_PATH, 'bot')







#functions

def format(data):
	if( data.find("\r\n") == -1):
		return  ("{0}\r\n".format(data))

	return data

def clean_str(data):
	if( data.find("\r\n") != -1):
		return data.strip()

	return data



def load_extra_paths():
	fake_root_path = os.getcwd()
	bot_path = os.path.join(fake_root_path, 'bot')

	
	sys.path.append(bot_path)


	#print(sys.modules)


