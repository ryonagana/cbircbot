# -*- coding: utf-8 -*- 

DEBUG_MODE = True

def format(data): #all irc messages must carry \r\n  and received data comes with \r\n too  to parse must be removed \r\n using split()
	return "{0}\r\n".format(data)


