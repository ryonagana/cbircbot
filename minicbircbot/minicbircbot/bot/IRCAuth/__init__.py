import os
from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface


class IRCAuth(IrcBotInterface):
    def __init__(self, irc = None):
        super().__init__(irc)

        self.module_name = "IRCAuth"
        self.register_command("!auth", self.do_auth_nick,  self.CMD_TYPE_BOTH, "my description")
    
    def do_auth_nick(self, handlers):
        irc, msghandler = handlers
        prefix, cmd, count_args = self.getMessageArgs(msghandler.message)  
        chan = irc.config.get("chans")



        if(count_args > 0):
            irc.ircSendMessage(chan, "No args are allowed here!")
            return

        username = os.getenv('CBIRCBOT_USER')
        passwd = os.getenv('CBIRCBOT_PASSWD')

    


        if not username or not passwd:
            irc.ircSendMessage(chan, "username and passwd not set, sorry!")
            return

        
        irc.identify.identify_nickname(self)



