# -*- coding: utf-8 -*- 

import socket
import sys
import os
import threading
import config
import datetime
import time
import re

import utils




class IrcClient(object):
	def __init__(self):
		self.conf = config.Config()
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	def initConnection(self):
		self.conf.open()
		self.sock.connect((self.conf.option['server'],int(self.conf.option['port']) ))

	def disconnect(self):
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()

	def send(self,data): # just send ordinary message  (just for internal commands)
		sock.send(utils.format(data))
	#send a message to a channel
	#this functions has 3 way  to operate
	#if channel is omitted  will send to all channels that bot is connected
	#if is ommited and the channel is not an array will send to  same channel in config.cfg
	#if channel is not ommited will send to channel in argument
	def sendMessage(self,message, channel=None,*args,**kwargs):

		if channel != None:
			send("PRIVMSG {0} :{1}".format(channel,message))
		else:
			if not isinstance( conf.option['channels'], (list,tuple) ):
				send("PRIVMSG {0} :{1}".format(conf.option['channels'],message))
			else:
				for c in channelList():
					send("PRIVMSG {0} :{1}".format(c,message))

	def sendMessageTo(self,message,person,*args,**kwargs):
		if message and person:
			send("PRIVMSG {0} :{1}".format(person,message))

	def parseServer(self,data, *args, **kwargs):

		nick = ""
		channel = ""
		identd = ""
		message = ""

		cleandata = data.replace('\r\n','') # cleaning string

		reg = re.search("^:(.+[aA-zZ0-0])!(.*) PRIVMSG (.+?) :(.+[aA-zZ0-9])$", cleandata )

		if data.find("PRIVMSG") != -1: #is a simple message
		
		
			if(reg):
				nick = reg.groups()[0] #store nickname
				identd = reg.groups()[1] # store ip identd
				channel = reg.groups()[2] # store channel
				message = reg.groups()[3] # store typed message
			
				userdata = {"nick":nick, "identd":identd,"channel":channel}

				self.isCommand(userdata, message); #SEND A array with  sender data 
				self.detectNicknameQuote(userdata, message)
				self.detectPrivateMessage(userdata,message)

				print "<{0}:{1}> {2}".format(nick,channel,message)



	def isCommand(self,user, data):

		if(data.startswith('!')):
			command = data.split('!')[1:]
			print "Comando digitado:",  command
			self.parseChannelCmd(user,command)


	def detectNicknameQuote(self,user,message):

		if(message.find(conf.option['nick']) != -1):
			if message.find("oi") != -1:
				self.sendMessage("Oi {0}!".format(user['nick']))


	def detectPrivateMessage(self,user,message):
		if not (user['channel'].startswith('#')):
			self.callPrivateMessage(user,message)



	def callPrivateMessage(self,user,message):
		sendMessageTo("Hey i dont like private messages", user['nick'])
		return

	def parseChannelCmd(user,cmd):

		#essentials commands
		command =  cmd[0].replace('\r\n','')
		if command.find("exit") != -1:
			if(user["nick"] == 'ryonagana'):
		
				sendMessage("Goodbye Cruel World",user['channel'])
				time.sleep(1) # i need at least 0.03ms to send message before close socket 1sec its a lot of time
				exit_gracefully()
			else:
				sendMessage('You are not my Master!! i just obey ryonagana')
				return

		if command.find("time") != -1:
			actualtime = datetime.datetime.now().__str__()
			sendMessage("Time is: {0}".format(actualtime), user['channel'])
			return


		'''add your commands here
		#example: command !helloworld
		'''

		if command.find('helloworld'):   #no character '!' please cause its already parsed and automatically detected
			#user['nickname'] =  the nick of the person who typed !helloword
			#user['channel'] = the channel of the  invoked command
			#user['identd'] = ident of the person

			#i just want to reply own the same channel where the command was invoked

			#this functions has 3 way  to operate
			#if channel is omitted  will send to all channels that bot is connected
			#if is ommited and the channel is not an array will send to  same channel in config.cfg
			#if channel is not ommited will send to channel in argument
			self.sendMessage("Hello World!", user['channel'])  
			return

