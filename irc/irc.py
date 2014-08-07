# -*- coding: utf-8 -*- 

#system libraries
import socket
import sys
import os
import threading
import datetime
import time
import re

#my library
import utils
import config
import response


class IrcClient(object):
	def __init__(self):

		self.isRunning = True
		self.data = ""
		self.hasJoined = False
		self.response = response.Response("response.txt")

		self.conf = config.Config()
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.initConnection()
		self.auth()
		#self.openResponse()

	def isClientRunning(self):
		return self.isRunning

	def isNotReceivingData(self):
		if not self.data:
			return False
		return True


	#be configurable via config.cfg (FUTURE)
	def wait(self):
		time.sleep(0.030)


	def ServerData(self):
		return self.sock.recv(4096)

	def initConnection(self):
		self.conf.open()
		self.sock.connect((self.conf.option['server'],int(self.conf.option['port']) ))
		print "Trying to connect {0}:{1}...".format(self.conf.option['server'], self.conf.option['port'])

	def disconnect(self):
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()

	def send(self,data): # just send ordinary message  (just for internal commands)
		self.sock.send(utils.format(data))
	#send a message to a channel
	#this functions has 3 way  to operate
	#if channel is omitted  will send to all channels that bot is connected
	#if is ommited and the channel is not an array will send to  same channel in config.cfg
	#if channel is not ommited will send to channel in argument
	def sendMessage(self,message, channel=None, *args,**kwargs):

		if channel != None:
			self.send("PRIVMSG {0} :{1}".format(channel,message))
		else:
			if not isinstance( self.conf.option['channels'], (list,tuple) ):
				self.send("PRIVMSG {0} :{1}".format(self.conf.option['channels'],message))
			else:
				for c in channelList():
					self.send("PRIVMSG {0} :{1}".format(c,message))

	def sendMessageTo(self,message,person,*args,**kwargs):
		if message and person:
			self.send("PRIVMSG {0} :{1}".format(person,message))

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

		if(message.find(self.conf.option['nick']) != -1):

			for question_pos in range(len(self.response.question)):
				if(message.find(self.response.question[question_pos]) != -1 ):
					answer =  self.response.answer[question_pos]

					if utils.DEBUG_MODE:
						print "Answer is: " + answer

					self.sendMessage(answer,user['channel'])

					#match =  re.match("{(.+[aA-zZ0-9])}", answer)

					#if(match):
					#	if(match.groups()[0].find("nick") != -1):
					#		nickname = match.groups()[0]
					#		answer.format(nick=nickname)
					#		self.sendMessage(answer,user['channel'])

						
						
					

		
		'''
		if(message.find(self.conf.option['nick']) != -1):
			
			for question_pos in range(len(self.response.question)):
				answer = self.response.answer[question_pos]

				match =  re.match("{(.+[aA-zZ0-9])}", answer)

				if(match):
					if(match.groups()[0].find("nick") != -1):
						nickname = match.groups()[0]
						answer.format(nick=nickname)
						self.sendMessage(answer,user['channel'])

				else:
					self.sendMessage(answer,user['channel'])
				break

		#	if message.find("oi") != -1:
		#		self.sendMessage("Oi {0}!".format(user['nick']))
		'''


	def detectPrivateMessage(self,user,message):
		if not (user['channel'].startswith('#')):
			self.callPrivateMessage(user,message)



	def callPrivateMessage(self,user,message):
		self.sendMessageTo("Hey i dont like private messages {0} fuck you!".format(user['nick']) , user['nick'])
		return

	def parseChannelCmd(self,user,cmd):

		#essentials commands
		command =  cmd[0].replace('\r\n','')
		if command.find("exit") != -1:
			if(user["nick"] == 'ryonagana'):
		
				self.sendMessage("Goodbye Cruel World",user['channel'])
				time.sleep(1) # i need at least 0.03ms to send message before close socket 1sec its a lot of time
				self.exit_gracefully()
			else:
				self.sendMessage('You are not my Master!! i just obey ryonagana')
				return

		elif command.find("time") != -1:
			actualtime = datetime.datetime.now().__str__()
			self.sendMessage("Time is: {0}".format(actualtime), user['channel'])
			return






	def exit_gracefully(self):
		self.sock.shutdown(socket.SHUT_RDWR)
		self.sock.close()
		sys.exit(0)

	def checkIsConnected(self,data):
		m = re.match('IP MODE', data, re.M | re.I)

		if m:
			return True
		return False


	#irc server always check if you are online send a PING and you  must respond with PONG  + ident
	def checkPingPong(self,data):
		if(self.data.find("PING") != -1):
			print "PING!"
			self.send("PONG {0}".format(data.split()[1]))
			print "!PONG"


	def auth(self): #create authorization to login
		self.send("NICK {0}".format(self.conf.option['nick']))
		self.send("USER {0} {1} {2} :testando".format(self.conf.option['nick'],self.conf.option['server'],"wololo"))

	def join(self,channel): #join in any server  with or without #
		if channel.startswith("#"):
			self.send("JOIN {0}".format(channel))
		else:
			self.send("JOIN #{0}".format(channel))

	#logger.info("-------------------- JOINED {0} --------------------".format(channel))


	def joinChannel(self,*args,**kwargs): #this function must be called once when connected to the server and must not be used


		chans = self.conf.option['channels'].split(';')
		#print "Chans: ", chans
		if chans:
			for c in chans:
				self.join(c)
			
		else:
			self.join(conf.option['channels'])