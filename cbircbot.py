import irc
from irc import irc
from irc import config
from irc import ircevents
import utils

if __name__ == "__main__":
	

	client = irc.IrcClient()



	try:
		while client.isClientRunning():

			data = client.ServerData()

			if(client.isNotReceivingData()):
				break

			if ircevents.IrcisConnected(data):
				print "---------------------------------- MOTD END ---------------------------------- "

				if not client.hasJoined:
					client.joinChannel()
					client.hasJoined = True

			if utils.DEBUG_MODE:
				print "[Server] " + data
			client.parseServer(data)
			client.checkPingPong(data)
			client.wait()
	except KeyboardInterrupt, Exception:
			client.disconnect()
			client.exit_gracefully()
