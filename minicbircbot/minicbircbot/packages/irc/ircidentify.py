import sys
import os

class IrcIdentify:
    def __init__(self, parent = None):
        self.parent = parent

    def detectIdentify(self, *args, **kwargs):
        nickname = self.parent.config.get('nickname')
        msg_detect = 'NOTICE {nick} :You are now identified for'.format(nick=nickname)

        msg = kwargs['msg']
        msg = msg.decode('utf8')

        print(msg + '\r\n\n')

        if msg.find(msg_detect) != -1:
            return True
        
        return False

    def identify_nickname(self, *args, **kwargs):

        try:
            os.environ['CBIRCBOT_PASSWD']
            pwd = os.environ['CBIRCBOT_PASSWD']
            self.parent.ircSend("PRIVMSG NICKSERV :identify {0}".format(pwd))
            return True
        except KeyError:
            print('Environment Var \'CBIRCBOT_PASSWD\' not found. its impossible to identify ')
            return False


        return False