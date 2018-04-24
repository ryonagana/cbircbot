import os
import sys
import time
import logging
import re
import importlib
from importlib.abc import Loader
import imp

import colorama
from colorama import Fore, Back, Style

"""
This Class has all irc handlers  and is intended  to create methods for IRC only


"""

__author__ = "Nicholas Oliveira <ryonagana@gmail.com>"
__date__ = "12 August 2014"

__version__ = "$Revision: 88564 $"
__credits__ = """Guido van Rossum, for an excellent programming language.
                 Jerónimo Barraco Marmól,  being  excellent programmer, gamer and friend.
"""

from minicbircbot.packages.config.config_json import ConfigJson
from minicbircbot.packages.sockets.sockethandler import IrcSocket
from minicbircbot.utils import format, clean_str, DEBUG_MODE, MODULES_LOADED, resetColors
from minicbircbot.packages.irc.irceventhandler import IrcEventhandler, IrcMessageEvent, IrcPrivateMessageEvent, \
    IrcJoinEvent, IrcPartEvent
import minicbircbot.bot

logger = logging.getLogger(__name__)


class ircClient:
    namespace = "minicbircbot.bot."
    
    def __init__(self, *args, **kwargs):
        
        self.use_envvars = False
        self.use_params = False
        cfg = {}
        
        for key, value in kwargs.items():
            if key == 'use_env':
                self.use_envvars = kwargs['use_env']
            if key == 'params':
                self.use_params = kwargs['params']
               
               #processing params from shell/cmd
                params = kwargs['params']
                cfg = {
    
                    'address': params['address'],
                    'port': int(params['port']),
                    'chans': params['channel'],
                    'nickname': params['nickname'],
                    'identd': params['identd'],
                    'console': False,
                    'modules': params['modules']
                }
                if not params['modules']:
                    params['modules'] = '*'
                    
                cfg['modules'] = cfg['modules'].split(';')
                
                

        self.config = ConfigJson("config.json", use_env=self.use_envvars)
        
        if self.use_params:
            self.config.setDefaultOpts()
            pass
        
      
        
        
        self.config.load()
        
        self.initModules()
        
        if DEBUG_MODE:
            print(Fore.YELLOW + "Loading Modules: ")
            print(Fore.YELLOW + self.config.get("modules"))
            print(Fore.YELLOW + MODULES_LOADED)
            print(Fore.YELLOW + "------------------------")
            resetColors()
        
        self.ircsocket = IrcSocket(self.config.get("address"), self.config.get("port"))
        
        self.isRunning = False
        self.isJoined = False
        self.isConnected = False
        
        self.server_message = []
        
        if self.config.get("console"):
            self.Console = IrcConsoleCommands(self)
            
            
            # teste
            # self.sock = socketserver.TCPServer( ("localhost", 9999), MainLoop)
            
            # def ServerMessages(self, data):
    
    def initModules(self):
        """ init all modules you wrote in config.json
            search in minicbircbot.bot.* for modules
            and create a new instance in the global variable
            MODULES_LOADED
        """
        global MODULES_LOADED
        
        for mod in self.config.get("modules"):
            # Who's bad?
            
            # i'm so evil that i'm using eval
            # the devil of programming
            # >=)
            try:
                module_loaded = self.instantiateModule(mod)
                MODULES_LOADED[mod] = module_loaded(self)
            
            
            
            
            
            
            except Exception as ex:
                
                print(Fore.RED + "-------------------------------------------------")
                print(Fore.RED + "Occurred an Exception in Module \"{0}\" and will not be loaded in the bot until you fix this module!".format(mod))
                print(Fore.RED + "Exception: {0}".format(ex))
                print(Fore.RED + "Please FIX it: bot/{0}/__init__.py  Check the Log".format(mod))
                print(Fore.RED + "-------------------------------------------------")
                print(Fore.RED + "Please Check the Log")
                
                logger.critical(
                    "Exception Occurred when tried  to load module: {0}. Please Check {1}/__init__.py - {2}".format(mod,
                                                                                                                    mod,
                                                                                                                    str(
                                                                                                                        ex)))
                resetColors()
        
        if DEBUG_MODE:
            with(open("modules.txt", 'w')) as fp:
                for m in sys.modules:
                    module_name = "{0}\n".format(m)
                    fp.write(module_name)
        pass
        
        print(" MODULES Running  ------------------------------------------:")
        for k in MODULES_LOADED:
            print(k)
        print("-----------------------------------------------------")
    
    def instantiateModule(self, module_name):
        """
            when the module is in memory it tried to create a new instance of the module
            returns the module object - ircBotInterface child class
        """
        
        inst = None
        module = None
        
        try:
            
            inst = __import__(self.namespace + module_name,
                              fromlist=module_name)  # importlib.import_module(namespace + module_name, module_name)
            return getattr(inst, module_name)
            
            #if DEBUG_MODE:
            #    print("Loaded: {0}.{1}".format(self.namespace, module_name))
        
        except Exception as ex:
            print(Fore.RED + "ERROR: Cannot Instantiate {0}".format(module))
            print(Fore.RED + "Exception: {0}".format(str(ex)))
            print(Fore.RED + "Please Check the Log")
            logger.critical(
                "Exception Occurred when tried  instantiate a module: {0} - {1}".format(module_name, str(ex)))
            resetColors()
            return None
    
    def reloadModules(self):
        global MODULES_LOADED
        
        print(Fore.RED + "-------------------------------------------------")
        print(Fore.RED + "MODULE RELOADING      (or die tryin)            ")
        print(Fore.RED + "------------------------------------------------")
        resetColors()
        
        for module_name in MODULES_LOADED:
            module_instance = MODULES_LOADED[module_name]
            try:
                print("Trying to Reload: {0}".format(self.namespace + module_name))
                
                if DEBUG_MODE:
                    with(open("external_modules.log", "w")) as fp:
                        fp.write(self.namespace + module_name)
                
                module = "{0}.{1}".format(self.namespace, module_name)
                imp.reload(minicbircbot.bot)
                
                # imp.reload(MODULES_LOADED[module_name])
            except Exception as ex:
                msg = "Exception Ocurred: {0}".format(str(ex))
                logger.critical(msg)
                print(msg)
            
            pass
    
    def auth(self):
        """ make the irc auth sending your credentials"""
        self.ircSend("NICK {0}".format(self.config.get("nickname")))
        self.ircSend("USER {0} {1} {2} :{3}".format(self.config.get("nickname"), self.config.get("address"),
                                                    self.config.get("identd"), 'Test'))
        logger.info("Auth Sent")
    
    def connect(self):
        """ create a new socket  and try to connect  the server """
        if self.ircsocket.createConnection():
            self.isRunning = True
            logger.info("Connected Successfully!")
    
    def ircSend(self, message):
        """ Send a Simple message to server """
        self.ircsocket.send(format(message))
    
    def ircSendMessageTo(self, receiver, message):
        """ intended only to send direct messages to someone (pvt messages) """
        if not receiver.startswith("#"):
            self.ircSend("PRIVMSG {0} :{1}".format(receiver, message))
    
    def ircSendMessageQuote(self, sender, receiver, message):
        """ Sends a message to the channel call the name of the receiver """
        if not sender or not message:
            return
        
        self.ircSend("PRIVMSG {0} :{1}".format(
            
            receiver,
            "{0}: {1}".format(sender, message)
        ))
    
    def ircSendMessage(self, channel, message):
        """ send a message directly to a channel """
        self.ircSend("PRIVMSG {0} :{1}".format(channel, message))
    
    def ircSetMode(self, channel, mode, *parameter):
        count = len(parameter)
        
        if not channel.startswith("#"):
            logger.warning("ircSendMessage failed {0} is not a valid channel".format(channel))
            return
            
            # makes the mode repeat  e.g :  count = 3.   mode_str = "ooo"
        mode_str = "+" + (mode * count)
        
        print("MODE {0} {1} {2} ".format(
            channel,
            mode_str,
            " ".join(parameter)
        ))
        
        """
        self.ircSend("MODE {0} {1} {2} ".format(
                                channel,
                                mode_str,
                                " ".join(parameter)

        ))
        """
        
        # print("<{0}> set {1} {2}".format())
    
    def ircPart(self, channel):
        """ just makes the bot leaves  the channel """
        temp_message = "cbircbot - rooling  da teats"
        
        if not channel.startswith("#"):
            self.ircSend("PART #{0} :{1}".format(channel, temp_message))
        
        self.ircSend("PART {0} :{1}".format(channel, temp_message))
    
    def ircJoin(self, channel):
        """ join the bot in a channel """
        if type(channel) == str:
            
            if (channel.startswith("#") != -1):
                self.ircSend("JOIN {0}".format(channel))
            else:
                self.ircSend("JOIN #{0}".format(channel))
    
    def ircDisconnect(self, channel):
        
        if channel.find("#") != -1:
            self.ircSend("PART {0} :\"Running with Scissors\"".format(channel))
    
    def JoinChannels(self, channels):
        """ join the bot in all channels in config.json  if just a simple string make a join, if channels is  a list
            make a simple join loop - obs this function  can only being called when  end of MOTD is detected
        """
        
        if type(channels) is (dict, list):
            for c in channels:
                self.ircJoin(c)
        
        elif type(channels) is str:
            self.ircJoin(channels)
    
    def detectEndMOTD(self, data):
        """ detects when motd is finished to show, can vary server for server """
        msg = data.decode('utf8')
        
        if msg.find(':End of /MOTD') != -1 or msg.find('/MOTD') != -1 :
            self.isConnected = True
            return True
        return False
    
    def receiveData(self):
        """ method to receive 4 kbytes """
        data = self.ircsocket.recv(4096);
        return data
    
    def receiveAsString(self):
        """ method convert  bytes to unicode """
        data = receiveData()
        return data.decode("utf-8")
    
    def PingPong(self, message):
        """ method when servers send a ping the bot responds with PONG """
        # message already comes in utf8 no need to convert again
        # is giving some  weird exceptions
        msg = message.decode("utf-8")
        if msg.find("PING") != -1:
            self.ircSend("PONG {0}".format(message.split()[1]))
    
    def ircEventHandler(self, data):
        """ this method is  the heart of the bot
            make all calling  trigger events repass data to parse
            to trigger bots events
        """
        
        self.PingPong(data)
        if self.detectEndMOTD(data):
            if not self.isJoined:
                self.JoinChannels(self.config.get("chans"))
                self.isJoined = True
                
                if self.config.get("console"):
                    self.Console.start()
        
        self.parseServerData(data)
    
    def isServerRunning(self, data):
        """ check if mainloop still running """
        if not self.isRunning:
            return False
        
        self.ircEventHandler(data)
        return True
    
    def deInitModules(self):
        """
            theres no need  to create a module deinitializator
            but im dealing with some asynchronous process
            i need to kill threads inside modules before bots stops
            or any ^C Signal is sent
            thats the purpose of this function  and is purely optional
            unless you use threads in your modules
        """
        for mod in MODULES_LOADED:
            try:
                if MODULES_LOADED[mod]:
                    MODULES_LOADED[mod].destroyModule()
            except Exception as ex:
                msg = "{0} has not destroyModule(). ignoring. Please see the log".format(mod)
                print(msg)
                logger.warning(msg)
                pass
        pass
    
    def exit_gracefully(self):
        """
            this method just make sure will not corrupt socket file descriptor
            just  end the main loop
            wait one second to socket  finish and close createConnection

        """
        
        exit_handler = IrcEventhandler()
        self.BotExitEvent(exit_handler)
        self.isRunning = False
        self.deInitModules()
        time.sleep(2)
        
        self.ircsocket.force_close()
        logger.info("Socket Closed With Success!")
    
    def parseServerData(self, message):
        """
            this method generates  the events for the bot and trigger them in all external modules
        """
        # decode the message to utf8, sanitize the string removing '\r\n' or the regex will fail so badly
        server_msg = clean_str(message.decode("utf-8"))
        
        # before make a check we must have sure is a message
        # PRIVMSG stand for 2 kinds of message, send to other person, or  regular message in the channel
        # the difference is the receiver
        
        
        if server_msg:
            self.BotServerDataSent(server_msg, None)
        
        if server_msg.find("PRIVMSG") != -1:  # is this a message?
            
            is_message = re.search("^:(.+[aA-zZ0-0])!(.*) PRIVMSG (.+?) :(.+[aA-zZ0-9])$",
                                   server_msg)  # strip all contents useful for me
            
            if is_message:  # regex is successfull
                
                
                data = {
                    
                    'sender': is_message.groups()[0],  # sender's nickname
                    'ident': is_message.groups()[1],  # ident
                    'receiver': is_message.groups()[2],  # channel or receiver's nickname
                    'message': is_message.groups()[3],  # message
                }
                
                #if DEBUG_MODE:
                #    print('DATA DEBUG: ')
                #   print(data)
                    
                    # if the receiver is a channel  trigger self.ReceivedMessageChannel, otherwise trigger self.ReceivedPrivateMessages
                if data['receiver'].startswith("#"):
                    
                    # means you are sending message directly to a channel
                    message_received = IrcMessageEvent.register(**data)
                    self.ReceivedMessageChannel(message_received)
                    
                    print(Fore.BLUE + "<" + Fore.WHITE + data['receiver'] + "> " + Fore.CYAN + data["message"])
                    resetColors();
                
                else:
                    
                    # means you are sending message directly to someone
                    message_received = IrcPrivateMessageEvent.register(**data)
                    self.ReceivedPrivateMessages(message_received)
                    
                    print(Fore.BLUE + "<" + Fore.WHITE + data['sender'] + ": " + data["receiver"] + "> " + Fore.CYAN +
                          data["message"])
                    resetColors()
        
        if server_msg.find("JOIN") != -1:  # join event?
            
            # message example
            #:ryonagana!vagrant@gsu.dbo.107.177.IP JOIN :#python
            is_join = re.search(":(.+[aA-zZ0-0])!(.*) JOIN :(.+?)$", server_msg)
            
            if is_join:
                data = {
                    
                    'sender': is_join.groups()[0],
                    'ident': is_join.groups()[1],
                    'channel_joined': is_join.groups()[2],
                }
                
                join_event = IrcJoinEvent(**data)
                self.ReceivedJoinEvent(join_event)
                
                print(Fore.YELLOW + "{0} Joined {1}".format(join_event.sender, join_event.channel_joined))
                resetColors()
        
        if server_msg.find("PART") != -1:  # join event?
            
            is_part = re.search(":(.+[aA-zZ0-0])!(.*) PART (.+?) :\"(.+[aA-zZ0-9])\"$", server_msg)
            
            if is_part:
                data = {
                    
                    'sender': is_part.groups()[0],
                    'ident': is_part.groups()[1],
                    'channel_part': is_part.groups()[2],
                    'quit_msg': is_part.groups()[3],
                }
                
                part_event = IrcPartEvent(**data)
                self.ReceivedPartEvent(part_event)
                print(Fore.YELLOW + "{0} Part {1}".format(join_event.sender, join_event.channel_joined))
                resetColors()
        
        if (len(self.server_message) <= 10):
            self.server_message.append(server_msg)
        else:
            self.server_msg = self.server_message[1:]
        
        
        
        # def  getModuleEvent(self)
        
        
        
        # send  event triggered to all modules loaded ReceivedMessageChannel
    
    def ReceivedMessageChannel(self, msghandler):
        """
        Event When someone send any message to all  channels when the bot is connected
        """
        
        for mod in MODULES_LOADED:
            if MODULES_LOADED[mod]:
                MODULES_LOADED[mod].onReceivedChannelMessage(self, msghandler)
        pass
        
        # send  event triggered to all modules loaded ReceivedPrivateMessages
    
    def ReceivedPrivateMessages(self, msghandler):
        """
            This event is triggered when someone send any message to the bot via PVT
        """
		
        message = msghandler.message.split(' ')
        count = len(message)
		
        
       
        if "!help" in message[0] and count == 1:
            self.ircSendMessageTo(msghandler.sender, " == Modules Installed ===")
            for mod in MODULES_LOADED:
                msg = MODULES_LOADED[mod].module_name
                self.ircSendMessageTo(msghandler.sender, msg)
                time.sleep(3)
            self.ircSendMessageTo(msghandler.sender, " == Modules END ===")
            return
			
		
        for mod in MODULES_LOADED:
            if MODULES_LOADED[mod]:
                MODULES_LOADED[mod].onReceivedPrivateMessage(self, msghandler)
        
        pass
    
    def ReceivedJoinEvent(self, msghandler):
        """
            ReceivedJoinEvent is triggered when anyone join the channel
        """
        
        for mod in MODULES_LOADED:
            if MODULES_LOADED[mod]:
                MODULES_LOADED[mod].onChannelJoined(self, msghandler)
        pass
    
    def ReceivedPartEvent(self, msghandler):
        """
            ReceivedPartEvent is triggered when anyone part the channel
        """
        for mod in MODULES_LOADED:
            if MODULES_LOADED[mod]:
                MODULES_LOADED[mod].onChannelPart(self, msghandler)
        pass
    
    def BotServerDataSent(self, data, msghandler):
        """
        BotServerDataSent is triggered when server sends  a full buffer of data
        """
        for mod in MODULES_LOADED:
            if MODULES_LOADED[mod]:
                MODULES_LOADED[mod].onDataSent(data, msghandler)
        pass
        
        # TODO - change event name and fix al calling  reflections in other modules
    
    def BotExitEvent(self, msghandler):
        """
            BotExitEvent is triggered when  you trigger any bot quitting service
            like  ^C or  when abruptly finish the bot process
            everty time when  exit_gracefully is called
        """
        
        for mod in MODULES_LOADED:
            if MODULES_LOADED[mod]:
                MODULES_LOADED[mod].onExit(self, msghandler)
        pass
        
        # def getServerMessages(self, lines = 2, size = 4096 ):
