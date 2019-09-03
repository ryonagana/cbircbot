#!/usr/bin/env python3
import os
import sys
import importlib

import minicbircbot
import minicbircbot.utils

try:
    import colorama
except ImportError:
    print("Colorama not Found.. Quitting..")
    sys.exit(0)



def check_root():
    try:
        if os.getuid() == 0 or os.geteuid() == 0:
            print("Dont Run as Root! privileges")
            sys.exit(0)
        return True
    except AttributeError:
        pass



if __name__ == "__main__":
    import platform
    try:
        if(platform.platform().startswith('Linux')):
            check_root()
        
        minicbircbot.utils.load_extra_paths()
        #minicbircbot.motd()
        
        #check if config.json exists
        try:
            with open('config.json', 'r') as f:
                pass
        except:
            print('config file not found. please create a new one\n\n')
            print('====================  END ========================')
            sys.exit(0)
            
            
            
        
        minicbircbot.init_bot()
    except Exception as m:
        print('An Error Ocurred while trying to run the bot. :' + m)
        sys.exit(0)
        
