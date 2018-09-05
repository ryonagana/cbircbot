import os
from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface


class IRCAuth(IrcBotInterface):
	    def __init__(self, irc = None):
        super().__init__(irc)


        self.owner = ["archdark", "ryonagana"]
        self.module_name = "IRCAuth"
        self.register_command("!authnick", self.do_auth_nick,  self.CMD_TYPE_BOTH, "my description")
    
    def do_auth_nick(self, handler):
        irc, msghandler = handlers
        prefix, cmd, count_args = self.getMessageArgs(msghandler.message)  
        chan = irc.config.get("chans")

        if(count_args > 0):
        	irc.ircSendMessageTo(handlers.sender, "No args are allowed here!")
        	return

        username = os.gentenv('CBIRCBOT_USER')
        passwd = os.gentenv('CBIRCBOT_PASSWD')


        if not username or not passwd:
        	irc.ircSendMessageTo(handlers.sender, "username and passwd not set, sorry!")
        	return

        
        if username.tolower() != msghandler.sender.tolower():
        	irc.setNick(msghandler.sender, username)

        irc.ircSendMessage(chan, "for this day and forward you will refer me by the name {0}, nheehehehe".format(username))
        irc.ircSendMessageTo("Nickserv", "identify {0}", passwd)



