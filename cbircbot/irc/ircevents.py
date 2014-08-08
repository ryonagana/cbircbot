# -*- coding: utf-8 -*- 
import os
import sys
import re


def  IrcisConnected(data):

	cleandata = data.replace('\r\n','')

	reg = re.search("^:(.+[aA-zZ0-0])!(.*).IP MODE (.*)$", cleandata )

	if(reg):
		return True
	return False
