#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from application import Application
import sys
import logging
from data_manager import DataManager

def main():
    logger = logging.getLogger('telethon')
    logger.propagate = False
    logger = logging.getLogger('vkbottle')
    logger.propagate = False
    logging.basicConfig(level='critical')
    app = Application()
    app.run()
    sys.exit()
    


if __name__ == '__main__':
    main()
