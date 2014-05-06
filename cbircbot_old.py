#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import socket
import sys
import os
import threading
import config
import datetime
import time
import re
import logging


logging.basicConfig(filename='chat.log',level=10)

logger = logging.getLogger(__name__)


conf = config.Config()
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
mainthread = False

isConnected = False
isJoined = False

DEBUG_MODE = True

RESPONSE_FILENAME = "response.txt"
RESPONSE_DATA = ""

RESP_QUESTION = []
RESP_ANSWER = []



def openResponse():
	global RESPONSE_DATA
	global RESP_QUESTION
	global RESP_ANSWER


	try:
		with open(RESPONSE_FILENAME,"rb") as f:
			for line in f.readlines():

				linestrip = line.replace('\r\n','')

				if(linestrip.startswith(">")):
					RESP_QUESTION.append(linestrip.replace(">",''))
				elif(linestrip.startswith("-")):
					RESP_ANSWER.append(linestrip.replace("-",''))
			#RESPONSE_DATA = f.readlines();


		#print RESP_QUESTION,RESP_ANSWER



	except Exception, msg:
		print msg

	print RESPONSE_DATA

def format(data): #all irc messages must carry \r\n  and received data comes with \r\n too  to parse must be removed \r\n using split()
	return "{0}\r\n".format(data)

def send(data): # just send ordinary message  (just for internal commands)
	sock.send(format(data))

def channelList(): #just convert  string list of channels in a list
	
	c = conf.option['channels'].split(';')	
	return c

def auth(): #create authorization to login
	send("NICK {0}".format(conf.option['nick']))
	send("USER {0} {1} {2} :testando".format(conf.option['nick'],conf.option['server'],"wololo"))

def join(channel): #join in any server  with or without #
	if channel.startswith("#"):
		send("JOIN {0}".format(channel))
	else:
		send("JOIN #{0}".format(channel))

	#logger.info("-------------------- JOINED {0} --------------------".format(channel))


def joinChannel(*args,**kwargs): #this function must be called once when connected to the server and must not be used


	chans = conf.option['channels'].split(';')
	#print "Chans: ", chans
	if chans:
		for c in chans:
			join(c)
			
	else:
		join(conf.option['channels'])

#exits gracefully irc closes the sockec and exits to your favorite O.S with sucess
def exit_gracefully():
	sock.shutdown(socket.SHUT_RDWR)
	sock.close()
	sys.exit(0)


def checkIsConnected(data):
	m = re.match('IP MODE', data, re.M | re.I)

	if m:
		return True
	return False


#irc server always check if you are online send a PING and you  must respond with PONG  + ident
def checkPingPong(data):
	if(data.find("PING") != -1):
		print "PING!"
		send("PONG {0}".format(data.split()[1]))
		print "!PONG"




#send a message to a channel
#this functions has 3 way  to operate
#if channel is omitted  will send to all channels that bot is connected
#if is ommited and the channel is not an array will send to  same channel in config.cfg
#if channel is not ommited will send to channel in argument
def sendMessage(message, channel=None,*args,**kwargs):

	if channel != None:
		send("PRIVMSG {0} :{1}".format(channel,message))
	else:
		if not isinstance( conf.option['channels'], (list,tuple) ):
			send("PRIVMSG {0} :{1}".format(conf.option['channels'],message))
		else:
			for c in channelList():
				send("PRIVMSG {0} :{1}".format(c,message))



def sendMessageTo(message,person,*args,**kwargs):
	if message and person:
		send("PRIVMSG {0} :{1}".format(person,message))



#thread to  type commands in console  (WIP)
def command():

	try:
		while True:
			cmd = raw_input('>> ')
			parseClient(cmd)
			time.sleep(0.01)
	except KeyboardInterrupt:
		console.join()

#starts the socket to receive data
def initConnection():
	conf.open()
	sock.connect((conf.option['server'],int(conf.option['port']) ))

#disconnect socket and frees  all data
def disconnect():
	sock.shutdown(socket.SHUT_RDWR)
	sock.close()	

#commands in bot console (WIP)
def parseClient(cmd):
	if cmd.find("exit") != -1:
		sendMessage("Adeus Mundo Cruel")
		exit() 

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
		sendMessage("Hello World!", user['channel'])  
		return


def isCommand(user, data):

	if(data.startswith('!')):
		command = data.split('!')[1:]
		print "Comando digitado:",  command
		parseChannelCmd(user,command)


def detectNicknameQuote(user,message):

	global RESP_ANSWER
	global RESP_QUESTION

	msg = message.replace('é','')

	if(message.find(conf.option['nick']) != -1):
		
		for q in range(len(RESP_QUESTION)):



			if( message.find(RESP_QUESTION[q]) != -1):

				answer = RESP_ANSWER[q]

				match = re.match("{(.+[aA-zZ0-9])}", answer)

				if(match):

					if(match.groups()[0].find("nick") != -1):
						nickname = match.groups()[0]
						answer.format(nick=nickname)
						sendMessage(answer,user['channel'])
				else:
					sendMessage(answer,user['channel'])
				


				





		


def detectPrivateMessage(user,message):
	if not (user['channel'].startswith('#')):
		callPrivateMessage(user,message)



def callPrivateMessage(user,message):
	format = "{0} says (pvt): {1}".format(user['nick'], message)
	logger.info(format)

		#sendMessageTo("Hey i dont like private messages", user['nick'])
	return

def parseServer(data, *args, **kwargs):

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
			message = reg.groups()[3].replace("\r\n",'') # store typed message
			
			userdata = {"nick":nick, "identd":identd,"channel":channel}

			isCommand(userdata, message); #SEND A array with  sender data 
			detectNicknameQuote(userdata, message)
			detectPrivateMessage(userdata,message)
			
			fmt = "<{0}:{1}>: {2}".format(nick, channel,  message)
			logger.info(fmt)
			print "<{0}:{1}> {2}".format(nick,channel,message)




#--------------------------------------- MAIN LOOP --------------------------------------
if __name__ == "__main__":
	initConnection()

	auth()
	openResponse()
	#console = threading.Thread(target=command)
	#console.start()


	try:
		while  True:
		
			
			data = sock.recv(4096)
			
			if not data:
				break

			if not isJoined:
				joinChannel()
				isJoined = False


			if DEBUG_MODE:
				print "Server: ", data
			parseServer(data)
			checkPingPong(data)
			time.sleep(0.030)	

	except KeyboardInterrupt, Exception:
			sock.close()
			exit_gracefully()
			#console.shutdown = True
			#console.join()

	#console.shutdown = True
	#console.join()

	exit_gracefully()

#-----------------------------------------------------------------------------------------