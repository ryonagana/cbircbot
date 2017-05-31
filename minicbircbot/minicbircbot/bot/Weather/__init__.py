
from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface
import urllib
import json
from urllib.request import urlopen
from urllib.parse import urlencode

class  Weather ( IrcBotInterface ):
    def __init__(self, irc = None):
        super().__init__(irc)
        
        self.owner = ['ryonagana']
        self.module_name = "Weather"
        
        self.baseurl = "https://query.yahooapis.com/v1/public/yql?"
        self.yql_query = 'select * from weather.forecast where woeid in (select woeid from geo.places(1) where text="{local}")'
        self.yql_url = ''

        self.register_command(",weather", self.show_weather, self.CMD_TYPE_MESSAGE, "Weather Yahoo API")
    
    def f_to_c(self, temp):
        return str( round((temp - 32) * 5.0/9.0, 1)) + 'C'
    
    def show_weather(self, handlers):
        irc, msghandler = handlers
        prefix, cmd, count_args = self.getMessageArgs(msghandler.message)
        
    
        
        if count_args > 0 and cmd[1]:
            
            #in case a city has space in their name
            place = cmd[1].split(' ')
            place = " ".join(place)
            
            self.yql_url = self.baseurl + urlencode({'q': self.yql_query.format(local=place)}) + "&format=json"
          
            chan_to_send = irc.config.get("chans")
            
            result = urlopen(self.yql_url).read().decode('utf-8')
            data = json.loads(result)
            if not data['query']['results']:
                irc.ircSendMessage(chan_to_send, "Place not found, sorry try again later")
                return
            
            channel = data['query']['results']['channel']
            location = channel['location']
            forecast = channel['item']['forecast'][0]
            loc = "{0} - {1}, {2}".format(location['city'], location['region'], location['country'])
            
            weather = "{0}, {1}, Max. {2}, Min.{3}".format(forecast['date'], forecast['text'],  self.f_to_c( float(forecast['high'])), self.f_to_c(float(forecast['low'])))
            message = "{0}, {1}".format(loc, weather)
            irc.ircSendMessage(chan_to_send, message)
            

        