import PySide
from PySide import QtCore as _qc
"""pyside only to treat threads. cause python multithreading support its too complicated for simple things
QThread has pefect support for thread
only votedown is  dependencies of pyside"""

logger = logging.getLogger(__name__)

''' Prototype '''

class IrcConsoleCommands(_qc.QThread):

    def __init__(self, irc, command = None,  commands_list = None):
        super().__init__()
        self.cmd = command
        self.cmd_list = commands_list
        self.irc = irc

    def run(self):


    

        #natives hardcoded commands
        try:
            while 1:
                user_type = input(">>  ")
                if user_type.startswith("say") != -1:
                    cmd = user_type.split()
                    if len(cmd) < 3:
                        print("say [#channel] message")
                    else:
                        self.irc.ircSend("PRIVMSG {0} :{1}".format(cmd[1], cmd[2]))

                if(user_type.startswith("quit") != -1):
                    chans = self.irc.config.get("chans")
                    
                    if type(chans) is (list, tuple):
                        for c in chans:
                            self.irc.ircSend("PRIVMSG {0} :{1}".format(c, "cbircbot - too drunk for you"))
                    elif type(chans) is str:
                        self.irc.ircSend("PRIVMSG {0} :{1}".format(chans, "cbircbot - too drunk for you"))
                        break

            time.sleep(2)
            self.irc.exit_gracefully()
            self.terminate()


        except (KeyboardInterrupt):
                self.terminate()
            
            




