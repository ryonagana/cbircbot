# -*- coding: utf-8 -*-


def format(data):
	if( data.find("\r\n") == -1):
		return  ("{0}\r\n".format(data))

	return data

def clean_str(data):
	if( data.find("\r\n") != -1):
		return data.replace("\r\n","")

	return data