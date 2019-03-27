import sys
import os

class IrcIdentify:
    def __init__(self, parent = None):
        self.parent = parent


    def identify_nickname(self):

        try:
            os.environ['CBIRCBOT_PASSWD']
            pwd = os.environ['CBIRCBOT_PASSWD']
            self.parent.ircSend("PRIVMSG NICKSERV :identify {0}".format(pwd))
            return True
        except KeyError:
            print('Environment Var \'CBIRCBOT_PASSWD\' not found. its impossible to identify ')
            return False


        return False