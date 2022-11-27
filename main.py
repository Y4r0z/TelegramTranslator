# -*- coding: utf-8 -*-
import os
from dotenv import load_dotenv
import logging as log 

from app.application import Application

def main():
    envPath = os.path.join(os.path.dirname(__file__), '.env')
    if not os.path.exists(envPath):
        log.error("Отсутсвует .env")
        print("Перед запуском программы создайте конфигурационный файл \".env\"!")
        raise Exception("Не найден конфигурационный файл .env")
        exit()
    load_dotenv(envPath) # os.environ.get()
    
    app = Application()


if __name__ == '__main__':
    main()