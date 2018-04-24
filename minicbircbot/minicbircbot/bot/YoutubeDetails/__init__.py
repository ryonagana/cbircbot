

from minicbircbot.packages.irc.ircbotinterface import IrcBotInterface
import json
import urllib.request
from bs4 import BeautifulSoup
import re


class YoutubeDetails(IrcBotInterface):
    def __init__(self, irc = None):
        super().__init__(irc)


        self.owner = ["ryongana"]

        self.module_name = "YoutubeDetails"

    def get_youtube_title(self,irc,msghandler,  *args, **kwargs):

        msg = msghandler.message
        ishttps = "http"

        if "https" in msg:
            ishttps = "https"

        link = "{0}://www.youtube.com".format(ishttps)
        link_no_www = "{0}://youtube.com".format(ishttps)
        link_www = "www.youtube.com"
        link_share = "{0}://youtu.be".format(ishttps)

        try:
            video_watch = msg.split('?')[1].split('v=')[1]
        except Exception as msg:

            return False

        if link_share in msg:
            url_final = "http://www.youtube.com/oembed?url={0}/{1}&format=json".format(link_share, video_watch)

        if link_www in msg:
            url_final = "http://www.youtube.com/oembed?url={0}/watch?v={1}&format=json".format(link_www, video_watch)

        if link in msg:
            url_final = "http://www.youtube.com/oembed?url={0}/watch?v={1}&format=json".format(link, video_watch)

        if link_no_www in msg:
            url_final = "http://www.youtube.com/oembed?url={0}/watch?v={1}&format=json".format(link_no_www, video_watch)

        if (msg.startswith(url_final) != -1):

            try:
                req = urllib.request.urlopen(url_final).read().decode('utf8')
                data = json.loads(req)

                msg = ' Type: \"{0}\" Title: \"{1}\" Author: \"{2}\" '.format(data['type'], data['title'],
                                                                              data['author_name'])

                self.irc.ircSendMessage(msghandler.receiver, msg)
            except:
                return False

        return True


    def get_site_title(self, irc, msghandler, *args, **kwargs):

        msg = msghandler.message

        url = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', msg)

        if not url:
            return False

        try:

            url = url[0]

            req = urllib.request.urlopen(url).read().decode('utf8')
            soup = BeautifulSoup(req)

            send_msg = "Title: \"{0}\" ".format(soup.title.string)


            self.irc.ircSendMessage(msghandler.receiver, send_msg)

        except Exception as ex:
            print(ex)
            return False

        return True



    def onReceivedChannelMessage(self, irchandler, messagehandler):

        super().onReceivedChannelMessage(irchandler, messagehandler)

        if self.get_youtube_title(irchandler, messagehandler):
            return
        else:
            self.get_site_title(irchandler, messagehandler)
            return









       
            
            
            
            
           
            
            
            
        
       