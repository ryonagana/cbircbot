cbIRCBOT 1.1
========

Simple Bot Written in Python. 

Atention: this is a ToyBot, if you need a real bot please use Willie

you can create your own funcionalities creating new modules

Dependencies:
  Colorama
>pip install colorama

Modules Included:
>HelloWorld  (example)

>PvtConsole  (bot remote control)

>WebServer   (remote control via browser) IN DEVELOPMENT

Just Choose your module  changing  config.json


How to Run
========
>./bot

Please Don't Run as Root. Ever

Added Identify to Server
========



How To: (UNIX / LINUX / MAC)
========
>export CBIRCBOT_PASSWD=yourpassword

Windows 
========
>set CBIRCBOT_PASSWD=yourpassword
>
>setx  CBIRCBOT_PASSWD=yourpassword




you must set an environment variable to store the password, its the safest simple solution
to not store any password on this project


PS:  All Modules has his own dependencies
cbIRCBot Core only uses colorama to make errors and warnings more visible


* TwitterBot Module Depends TwitterApi
* WebServer Modules Depends Tornado
* YoutubeDetails depends on BeautifulSoup4


If you dont want to deal with dependencies just disable the module in config.json
