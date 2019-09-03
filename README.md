cbIRCBOT 1.1.2
========

Simple Bot using Python. 

Atention: this is a **ToyBot**, if you need a real bot please use Willie

you can create your own funcionalities creating new modules for the bot

Dependencies:
  Colorama
>pip install colorama

Modules Included:
>HelloWorld  (example)

>PvtConsole  (bot remote control)

>WebServer   (remote control via browser) IN DEVELOPMENT

>**Weather** - Weather plugin is disabled as default due  Yahoo dropping their weather API

Just Choose your module  changing  config.json


**Don't forget to rename CONFIG.JSON.SKEL  to CONFIG.JSON**


How to Run
========
>./bot

Please Don't Run as Root. Ever

Added Identify to Server
========
You can Identify your  nickname  you need to set in config.json  auth: true
and set  env var  CBIRCBOT_PASSWD=yourpassword


How To Identify: (UNIX / LINUX / MAC)
========
>export CBIRCBOT_PASSWD=yourpassword

Windows 
========
>set CBIRCBOT_PASSWD=yourpassword
>
>setx  CBIRCBOT_PASSWD=yourpassword


