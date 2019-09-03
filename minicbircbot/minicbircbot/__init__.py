#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import getopt
from minicbircbot.packages.irc import ircClient
from minicbircbot.utils import resetColors
import time
import logging
import colorama
import asyncio
from colorama import Fore, Back, Style

# logging

logging.basicConfig(filename='cbircbot.log', level=logging.INFO)
logger = logging.getLogger(__name__)

if 'USE_ENVVARS' not in globals():
    global USE_ENVVARS
    USE_ENVVARS = False


def motd():
    msg = ""
    try:
        with(open("motd.txt", "r")) as f:
            for c in f.read():
                msg += c
    except:
        pass
    
    print(Fore.YELLOW + msg)
    resetColors()

def usage():
    print("\n"
          "bot.py or run.sh\n"
          "-i --identd=<YOUR IDENT>\n"
          "-a --address=<SERVER>\n "
          "-n --nick=<NICKNAME>\n"
          "-m --modules=<MODULES> - please use semicolon\n"
          "-p --port=<PORT NUMBER> - number only\n"
          "-c -channel=<CHANNEL> - use # or ## if neede, eg:  ##mychannel"
          "\n")


def init_bot():
    global USE_ENVVARS
    args_param = {}
    data = None
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hevi:a:n:m:p:c:",
                                   ['help', "env-vars", 'version', 'identd=', 'address=',
                                                                              'nick=', 'modules=', 'port=', 'channel='
                                    ])
        for o, a in opts:
            
            if o in ('-i', '--identd'):
                args_param['identd'] = a
        
            if o in ('-a', '--address'):
                args_param['address'] = a
                
            if o in ('-n', '--nick'):
                args_param['address'] = a
            
            if o in ('-m', '--modules'):
                if not a:
                    args_param['modules'] = '*'
                else:
                    args_param['modules'] = a
            
            if o in ('-p', '--port'):
                args_param['port'] = a
                
            if o in ('-c', '--channel'):
                args_param['channel'] = a
            
            if o == '-h':
                usage()
                sys.exit(0)
            elif o in ('-e', '--env'):
                print('LOADING ENVIRONMENT VARS')
                print('IF FAILS WILL LOAD config.json')
                USE_ENVVARS = True
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(0)
    
    colorama.init()
    
    if args_param:
        
        irc = ircClient(params=args_param)
    else:
        irc = ircClient()
    
    if not irc.isConnected:
        irc.connect()
        irc.auth()
   



    loop = asyncio.get_event_loop()


    while irc.isRunning:
        
        try:

            data = irc.receiveData()
            irc.ircEventHandler(data)
            time.sleep(0.2)
            loop.run_until_complete(irc.parseServerData(data))
            data = data.decode('utf-8')
            print(data)
        
        except KeyboardInterrupt:
            print(Fore.YELLOW + "Waiting 2 seconds")
            print(Fore.RED + "Closing Sockets")
            irc.exit_gracefully()
            logger.info("Successfully Closed")
            loop.stop()
            break
