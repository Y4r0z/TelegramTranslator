# -*- coding: utf-8 -*-
from application import Application
import sys
import logging

def main():
    logger = logging.getLogger('telethon')
    logger.propagate = False
    logger = logging.getLogger('vkbottle')
    logger.propagate = False
    app = Application()
    app.run()
    sys.exit()



if __name__ == '__main__':
    main()
