# -*- coding: utf-8 -*-
from data_manager import DataManager
from messages.media import Media, MediaType
import json
import os

from telethon import TelegramClient
from vkbottle import API
#Формат api dict{'vk_token':"", 'tg_id':0000, 'tg_hash':""}

class FileManager:
    __instance = None
    Path =\
    {
        'config' : 'config/',
        'temp' : 'Temp/',
        'chats' : 'config/chats.json',
        'api' : 'config/api.json'
    }
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(FileManager, cls).__new__(cls)
            cls.__instance.__init()
        return cls.__instance

    def __init(self):
        self.data = DataManager()
        if not os.path.exists(self.Path['temp']):
            os.makedirs(self.Path['temp'])

        if not os.path.exists(self.Path['config']):
            os.makedirs(self.Path['config'])
        
    
    async def downloadTgMedia(self, event, bot_client):
        filename = event.file.name
        path = await bot_client.download_media(event.media, self.Path['temp'])
        return Media(filename, MediaType.FromEvent(event), path)
    
    def saveChats(self):
        tg = [i.toDict() for i in self.data.tgChats]
        vk = [i.toDict() for i in self.data.vkChats]
        chats = {'tg' : tg, 'vk': vk}
        with open(self.Path['chats'], 'w') as file:
            json.dump(chats, file)
         
    def loadChats(self):
        '''
        Возвращает словарь данного вида:
        "tg":
            [
                {name, id}, ..
            ]
        "vk":
            [
                {name, id, subscriptions}, ..
            ]
        '''
        if not self.chatExists():
            raise Exception("Файл с чатами еще не создан.") 
        with open(self.Path['chats'], 'r') as file:
            data = json.load(file)
        return data


    def loadApi(self) -> dict:
        '''
        Возвращает словарь данного вида:
        dict{'vk_token':string, 'tg_id':int, 'tg_hash':string}"
        '''

        if not self.apiExists():
            raise Exception("Файл с APi еще не создан.") 
        with open(self.Path['api'], 'r') as file:
            data = json.load(file)
        return data

    def saveApi(self, api_dict : dict):
        '''
        На вход метода идёт словарь данной структуры:
        dict{'vk_token':string, 'tg_id':int, 'tg_hash':string}
        '''

        if len(api_dict) != 3 or not api_dict['vk_token'] or not api_dict['tg_id'] or not api_dict['tg_hash']:
            raise Exception("Неверный формат входного словаря." +
            "\nВходные данные должны соответствовать формату: dict{'vk_token':string, 'tg_id':int, 'tg_hash':string}")
        with open(self.Path['api'], 'w') as file:
            json.dump(api_dict, file)


    def chatExists(self):
        '''
        Проверка на существование конфига с чатами.
        '''
        return os.path.exists(self.Path['chats'])
    def apiExists(self):
        '''
        Проверка на существования конфигурации API.
        '''
        return os.path.exists(self.Path['api'])
    
    def inputApi(self) -> dict:
        '''
        Ввод и проверка api для Телеграм и ВК.
        '''
        print("Введите данные api")
        vk = self._inputApiVk()
        tg = self._inputApiTg()
        return {"vk_token":vk, "tg_id":tg[0], "tg_hash":tg[1]}
    
    def _inputApiVk(self):
        while True:
            try:
                token = input("Токен VK (vk_token): ")
                API(token)
                break
            except:
                print("Неверный токен!")
        return token
    def _inputApiTg(self):
         while True:
            try:
                tg_id = int(input("Telegram api ID (tg_id): "))
                tg_hash = input("Telegram api hash (tg_hash): ")
                TelegramClient('sessions/session', tg_id, tg_hash)
                break
            except:
                print('Неверные данные Telegram API!')
         return (tg_id, tg_hash)

        
    
