#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from application import Application
import sys
import logging
from data_manager import DataManager

def main():
    logging.getLogger('telethon').propagate = False
    logging.getLogger('vkbottle').propagate = False
    logging.getLogger('asyncio').propagate = False
    app = Application()
    app.run()
    sys.exit()
    


if __name__ == '__main__':
    main()
