# -*- coding: utf-8 -*- 

DEBUG_MODE = True

def format(data): #all irc messages must carry \r\n  and received data comes with \r\n too  to parse must be removed \r\n using split()
	return "{0}\r\n".format(data)


def sanitize(data):
	if(data.find("\r") or data.find('\n')):
		return data.split("\r\n")
	elif(data.find('\r\n')):
		return return data.split("\r\n")