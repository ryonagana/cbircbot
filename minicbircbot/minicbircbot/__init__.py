#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from minicbircbot.packages.irc import ircClient

import logging



# logging
logging.basicConfig(filename='email.log', level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":

	i = ircClient()