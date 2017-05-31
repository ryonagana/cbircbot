import time
import sys
import os
import importlib
import imp


import minicbircbot.bot.PvtConsole.cons

from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface
from minicbircbot.utils import DEBUG_MODE, MODULES_LOADED

class PvtConsole(IrcBotInterface):
    """
        Main Controller of the bot. its not dependency if this module  is disabled
        wont serve no commands to control the bot via PVT.
    """

    def __init__(self, irc = None):
        super().__init__(irc)

        self.owner = ["vagrant", "ryonagana"]

        self.module_name = "PvtConsole"

        self.namespace = "minicbircbot.bot."

        self.register_command("!say", self.sayToChannel, self.CMD_TYPE_PVT, "say something in the channel")
        self.register_command("!reload", self.reloadModules, self.CMD_TYPE_PVT, "reload all  external modules")
        self.register_command("!op", self.giveOp, self.CMD_TYPE_BOTH, "give op")
        self.register_command("!part", self.disconnectBot, self.CMD_TYPE_PVT, "get of a channel")
        self.register_command("!join", self.joinBot, self.CMD_TYPE_PVT, "enters in a channel")
        self.register_command("!names", self.showNames, self.CMD_TYPE_PVT, "show names")
        #self.register_command("!console", self.openConsole, self.CMD_TYPE_BOTH, "Open Console")
        #self.register_command("!load_module", self.loadModules_cmd, self.CMD_TYPE_BOTH, "Open Console")



        self.data = ""

    def onChannelJoined(self, irchandler, messagehandler):
        super().onChannelJoined(irchandler, messagehandler)


        #example of greeting
        irchandler.ircSendMessage(messagehandler.channel_joined, "Oi {0} Seja Bem Vindo ao {1}".format(messagehandler.sender, messagehandler.channel_joined ) )


    def onChannelPart(self, irchandler, messagehandler):
        super().onChannelPart(irchandler, messagehandler)
        print("SAIU")

    def onReceivedPrivateMessage(self, irchandler, messagehandler):
        super().onReceivedPrivateMessage(irchandler, messagehandler)


    def onReceivedChannelMessage(self, irchandler, messagehandler):
        super().onReceivedChannelMessage(irchandler, messagehandler)

    def onExit(self, irchandler, messagehandler):
        super().onExit(irchandler,messagehandler)

        #channel = irchandler.config.get("chans")

        #irchandler.ircSend("PART {0} :Screw You Guys, I'm Going Home.. - CARTMAN,Eric!".format(channel))



    def onDataSent(self, data, msghandler):
        super().onDataSent(self, data)
        self.data = data



    def loadModules_cmd(self, handlers):
        irc, msghandler = handlers
        prefix, cmd, count_args = self.getMessageArgs(msghandler.message)

        if(count_args == 1):
            try:
                if not imp.find_module(self.namespace+cmd[1]):
                    irc.ircSendMessageTo(msghandler.sender, "Module {0} Not found".format(cmd[1]))
                else:
                    global MODULES_LOADED
                    module_instance = irc.instantiateModule(mod)
                    module_name = cmd[1]
                    MODULES_LOADED[module_name]  = module_instance(irc)
                    irc.ircSendMessageTo(msghandler.sender, "Module {0} Load With Sucess".format(cmd[1]))
    
            except ImportError as import_error:
                    irc.ircSendMessageTo(msghandler.sender, "Module {0} Not found".format(cmd[1]))
        


    def giveOp(self, handlers):
        irc, msghandler = handlers
        prefix, cmd, count_args = self.getMessageArgs(msghandler.message)


        if count_args >= 2:
            irc.ircSetMode(cmd[1], "o", *cmd[2:])

        #if not msghandler.sender in self.owner:
        #	irc.ircSendMessageTo(msghandler.sender, "[Denied]")

        #irc.ircSetMode(cmd[1], "o", cmd[2] )



    def openConsole(self, handlers):
        irc, msghandler = handlers
        prefix, cmd, count_args = self.args(msghandler.message)


        mod_names = [ mod for mod in MODULES_LOADED ]

        motd = [
            'Welcome {0} to the cbircbot main control'.format(msghandler.sender),
            'type !help <module name>  to show all registered commands  in a certain module',
            'Modules Registered: {0} '.format(  ' '.join(mod_names)),
            '>>',
        ]


        for m in range(len(motd)):
            irc.ircSendMessageTo(msghandler.sender, motd[m])
            time.sleep(1)




    def showNames(self, handlers):

        irc, msghandler = handlers
        prefix, cmd, count_args = self.args(msghandler.message)

        print("===SHOW NAMES:===")

        if not count_args == 1:
            irc.ircSendMessageTo(msghandler.sender, "names: Invalid paramateres")
            irc.ircSendMessageTo(msghandler.sender, "syntax is: !names #channel")
            return



        cmd_names = "NAMES {0}".format(cmd[1])
        #print ("RUN: " + cmd)
        irc.ircSend(cmd_names)

        if self.data.find("NAMES") != -1:
            print ("Printing Data Names")
            print (self.data)
        #	print ("NAMES RODOU!")
        #	print (data)




    def reloadModules(self, handlers):


        irc, msghandler = handlers

        prefix, cmd, c = self.args(msghandler.message)

        print (prefix,cmd,c)

        if  c == 0 and msghandler.sender in self.owner:
            chans = irc.config.get("chans")
            #this doesnt work :( modules still the same  i just want to reload them runtime but nothing happens
            #FIX ME
            irc.reloadModules()
            irc.ircSendMessage(chans, "::Reloading Matrix Proudly Running in Win95 HUE:: ")



    def sayToChannel(self, handlers):

        irc, msghandler = handlers
        prefix, command, count = self.args(msghandler.message)



        if not msghandler.sender in self.owner:
            print("SENDER: {0}".format(msghandler.sender) )
            irc.ircSendMessageTo(msghandler.sender, "you are not my owner!")
            return

        #avoid split spaces in the messages
        channel = command[1]
        msg =  str(" ".join(command[2:]))
        irc.ircSendMessage(channel, msg)

        #print(prefix, msg)


    def disconnectBot(self, handlers):



        irc, msghandler = handlers
        prefix, command, count = self.CMD_Args(msghandler.message)

        chans = irc.config.get("chans")


        if count == 1 and command[1] == "all" and msghandler.sender in self.owner  :
            if type(chans) is (list, tuple):

                for c in chans:
                    irc.ircDisconnect(c)
                    print("Part {0}".format(c))
                    irc.ircSendMessage(msghandler.sender, "Disconnected from {0} with success".format(c))


            if type(chans) is str:
                irc.ircDisconnect(chans)
                print("Part {0}".format(chans))
                irc.ircSendMessage(msghandler.sender, "Disconnected from {0} with success".format(chans))
        else:
            return
            #irc.ircSendMessage(msghandler.sender, "[Command Failed]")


    def joinBot(self, handlers):

        irc, msghandler = handlers
        prefix, command, count = self.CMD_Args(msghandler.message)

        chans = irc.config.get("chans")

        if count == 1 and command[1].find("#") != -1 and msghandler.sender in self.owner:
            irc.JoinChannels(chans)
