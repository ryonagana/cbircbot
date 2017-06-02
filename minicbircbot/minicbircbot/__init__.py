#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import getopt
from minicbircbot.packages.irc import ircClient
from minicbircbot.utils import resetColors


import logging
import colorama
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
        with(open("motd.txt","r")) as f:
            for c in f.read():
                msg += c
    except:
        pass
    
    print(Fore.YELLOW + msg)
    resetColors()



def usage():
    pass

def init_bot():
    global USE_ENVVARS

    
    try:
        
        opts, args = getopt.getopt(sys.argv[1:], "hev", ['help', "env-vars"])
        for o,a in opts:
            if o == '-h':
                usage()
            elif o in ('-e', '--env'):
                print('LOADING ENVIRONMENT VARS')
                print('IF FAILS WILL LOAD config.json')
                USE_ENVVARS = True
            
            

    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(0)
    
    colorama.init()
    irc = ircClient()
    
    
    if not irc.isConnected:
        irc.connect()
        irc.auth()
    
    while irc.isRunning:
    
        try:
            data = irc.receiveData()
            irc.isServerRunning(data)
            #print (data)
                
        except (KeyboardInterrupt):
            print(Fore.YELLOW + "Waiting 2 seconds")
            print(Fore.RED + "Closing Sockets")
            logger.info("Desconnecting Socket")
            irc.exit_gracefully()
            logger.info("Successfully Closed")
            break

        