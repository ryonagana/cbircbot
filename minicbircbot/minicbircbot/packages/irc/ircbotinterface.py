# -*- coding: utf-8 -*-

import os
import sys
import time
from minicbircbot.utils import MODULES_LOADED
from minicbircbot.packages.irc.irccommand import IrcCommand

"""
This Class is an Abstract Class to make all modules with the  same class signature


"""

__author__ = "Nicholas Oliveira <ryonagana@gmail.com>"
__date__ = "12 August 2014"

__version__ = "$Revision: 88564 $"
__credits__ = """Guido van Rossum, for an excellent programming language.
                 Jerónimo Barraco Marmól,  being  excellent programmer, gamer and friend.
"""


CMD_MESSAGE = 2
CMD_PVT     = 4
CMD_BOTH    = 6



class IrcBotInterface:

    #run permissions
    BOT_RUN_NONE = 1
    BOT_RUN_USER = 2
    BOT_RUN_VOICE = 4
    BOT_RUN_OP = 8
    BOT_RUN_ALL = 16





    def __init__(self, irc = None):
        self.module_name = ""
        self.owner = [] #owner of the bot  if you want to retrict a command being run by only one person
        self.version = "" #version
        self.author = "" #author name
        self.permissions = self.BOT_RUN_ALL # permissions
        self.reg_command = {}
        self.irc = None
        
        for owner in irc.config.get('owners'):
            self.owner.append(owner)

        if irc:
            self.irc = irc



        self.CMD_TYPE_MESSAGE   = 2
        self.CMD_TYPE_PVT       = 4
        self.CMD_TYPE_BOTH      = 6
        self.CMD_TYPE_JOIN      = 8
        self.CMD_TYPE_PART      = 10

        self.generateHelp()




    def generateHelp(self):
        #if self.module_name:
        self.register_command("!help", self.module_usage, self.CMD_TYPE_PVT, "Show Module Help")


    def module_usage(self, handlers):
        irc, msghandler = handlers
        prefix, cmd, count_args = self.getMessageArgs(msghandler.message)
        
        
        """
            if(count_args == 0 and msghandler.sender in self.owner):
            irc.ircSendMessageTo(msghandler.sender, "==Installed Modules==")
            for nome in MODULES_LOADED:
                msg = "\t\t" + nome
                irc.ircSendMessageTo(msghandler.sender, msg)
                time.sleep(3)

            irc.ircSendMessageTo(msghandler.sender, "== END Installed Modules==")
            return

        """
        
        if count_args == 1:
            if cmd[1].find(self.module_name) != -1  and msghandler.sender in self.owner:


                help = "Module: {0} ==============".format(self.module_name)
                irc.ircSendMessageTo(msghandler.sender, help)


                for c in self.reg_command:
                    if c.find("help") == -1:
                        help_module = self.reg_command[c]
                    
                        print (help_module.prefix + c + " - " +  help_module.cmd_description)
                        m = "\t{0}{1} - {2}".format(help_module.prefix, c, help_module.cmd_description)
                        irc.ircSendMessageTo(msghandler.sender, m)
                        time.sleep(3) #avoid flood freenode has a  huge protection against flood

                help = "=========END OF HELP==========="
                irc.ircSendMessageTo(msghandler.sender, help)
        
        pass





    def args(self, args):
        """ gets the irc message  and split into  command and arguments """
        prefix = args[:1]
        command = args[1:].split(' ')


        return (prefix, command, len(command[1:]))
        #return args.split()

    def  getMessageArgs(self, args):
        """ same of args with better name  cause args is too generic and clunky name """
        return self.args(args)

    def CMD_Args(self, args):
        return self.args(args)

    def isCommand(self,msg, prefix):
        """ Check is message is a command """
        cmd = msg.split()
        if cmd[0].startswith(prefix):
            return True
        return False




        

    def register_command(self, command, func_callback, access = 2, description = ""):
        """ Register new command in the module
            All commands names mus be unique. im trying to figure how to not conflict names
            
        """
        if command and func_callback:


            prefix = command[:1]
            cmd = command[1:]


            gather = {

                'prefix'            : prefix,
                'func_callback'     : func_callback,
                'access'            : access,
                'cmd_description'   : description

            }

            self.reg_command[cmd] = IrcCommand()
            self.reg_command[cmd].load(**gather)

            #self.reg_command[cmd] = (prefix, func_callback, access)


    def getCommandAccess(self, cmd):
        if cmd in self.reg_command:
            return self.reg_command[cmd].access
        return None

    def exec_cmd(self,command, handlers, *args, **kwargs):
        """ execute  the command when called  it doesnt run in array
            if the right name is passed  they just call once.

        """
        if command in self.reg_command:
            #self.reg_command[command][1](handlers)
            self.reg_command[command].run(handlers)





    def onReceivedPrivateMessage(self, irchandler, messagehandler):
        """ abstract method when  the bot receives a private message """
        prefix, command, count  = self.args(messagehandler.message)

        access = self.getCommandAccess(command[0])

        
        if(command[0] == 'help' and prefix == '!'):
            self.exec_cmd('help', (irchandler, messagehandler))
            return
            
        if access == self.CMD_TYPE_PVT or access == self.CMD_TYPE_BOTH:
            self.exec_cmd(command[0], (irchandler, messagehandler))

        pass

    def onReceivedChannelMessage(self, irchandler, messagehandler):
        """ abstract method when  the bot receives message in channel
            it captures all messages in channel no exceptions.  you must program the module
            how to filter  the content in the channel
        """
        prefix, command, count  = self.args(messagehandler.message)
        access = self.getCommandAccess(command[0])

        if access == self.CMD_TYPE_MESSAGE or access == self.CMD_TYPE_BOTH:
            self.exec_cmd(command[0], (irchandler, messagehandler))

        pass

    def onChannelPart(self, irchandler, messagehandler):
        """
        abstract method when someone parts the channel trigger  this event
        """

        prefix, command, count  = self.args(messagehandler.message)
        access = self.getCommandAccess(command[0])

        if access == self.CMD_TYPE_PART:
            self.exec_cmd(command[0], (irchandler, messagehandler))
        pass

    def onChannelJoined(self, irchandler, messagehandler):
        """
        abstract method when someone join the channel   this event is triggered
        """

        prefix, command, count  = self.args(messagehandler.message)
        access = self.getCommandAccess(command[0])

        if access == self.CMD_TYPE_JOIN:
            self.exec_cmd(command[0], (irchandler, messagehandler))
        pass

    def onNickChanged(self, irchandler, messagehandler):
        """
        when someone changes the nick in the channel the bot triggers this event
        """
        pass



    #Events not IRC Related but Bot Related below

    def onExit(self, irchandler, messagehandler):
        """
        Tnis Event is not IRC Related. its when the bot is triggered to close (^C or any signal to exit and trigger exit_gracefully() )
        """

        prefix, command, count  = self.args(messagehandler.message)
        access = self.getCommandAccess(command[0])
        pass

    def onDataSent(self, data, irchandler):
        pass



    def DestroyModule(self):
        pass


