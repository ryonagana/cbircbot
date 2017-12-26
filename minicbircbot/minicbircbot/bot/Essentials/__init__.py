import datetime
import os
import sys


from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface


class Essentials(IrcBotInterface):
    def __init__(self, irc = None):
        super().__init__(irc)
        self.owner = ["ryonagana"]

        self.register_command("!auth", self.doAuth, self.CMD_TYPE_BOTH, "will try to make bot identify")
        
        

    def doAuth(self, handler):
        irc, msghandler = handler
        prefix, command, count = self.args(msghandler.message)
        password = os.environ.getenv('CBIRCBOT_PASSWD')
        chan = irc.config.get("chans")
        
        if not password:
            if self.owner is list:
                irc.ircSendMessageTo(self.owner[0], "Sorry, ENVVAR not set, impossible to auth")
            else:
                irc.ircSendMessageTo(self.owner, "Sorry, ENVVAR not set, impossible to auth")
            return

        irc.ircSendMessageTo(chan, ":: TRYING TO IDENTIFY NICKNAME AUTH ::")
        irc.ircSend("/msg nickserv identify {0}" .format(password))
        
    