# -*- coding: utf-8 -*-
if not'DEBUG_MODE' in globals():
	global DEBUG_MODE 
	DEBUG_MODE = False

if not 'MODULES_LOADED' in globals():
	global MODULES_LOADED
	MODULES_LOADED = {}

def format(data):
	if( data.find("\r\n") == -1):
		return  ("{0}\r\n".format(data))

	return data

def clean_str(data):
	if( data.find("\r\n") != -1):
		return data.replace("\r\n","")

	return data