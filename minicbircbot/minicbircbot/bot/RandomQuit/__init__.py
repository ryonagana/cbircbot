import sys
import os
import random

from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface


class RandomQuit(IrcBotInterface):
    def __init__(self, irc=None):
        super().__init__(irc)
        
        self.module_name = "RandomQuit"
        self.filename = "quit.txt"
        
        self.phrases = []
        self.linecount = 0
        
        if not os.path.isfile(self.filename):
            with open(self.filename, "w") as f:
                f.write("#File Generated Automatically\n")
                f.write("Screw You Guys, I'm Going Home!. CARTMAN, Eric\n")
                f.close()
                self._loadfile(self.filename)
        else:
            self._loadfile(self.filename)
    
    def _loadfile(self, filename):
        fp = open(filename, "r")
        
        # self.phrases = [ l.strip()  for l in fp.readlines()]
        for l in fp.readlines():
            if not l.startswith("#"):
                self.phrases.append(l)
        
        self.linecount = len(self.phrases)
        fp.close()
    
    def sortPhrases(self, irchandler, messagehandler):
        num = random.randint(0, self.linecount)
        channel = self.irc.config.get("chans")
        message = random.choice(self.phrases)
        
        irchandler.ircSend("PART {0} :{1}".format(channel, message))
    
    def onExit(self, irchandler, messagehandler):
        super().onExit(irchandler, messagehandler)
        
        self.sortPhrases(irchandler, messagehandler)
    
    def onChannelPart(self, irchandler, messagehandler):
        super().onChannelPart(irchandler, messagehandler)
        
        self.sortPhrases(irchandler, messagehandler)
        
        # print("SAIU")
