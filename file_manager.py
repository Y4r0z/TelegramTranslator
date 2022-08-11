# -*- coding: utf-8 -*-
from data_manager import DataManager
from messages.media import Media, MediaType
import json
import os
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
        if not self.chatExists():
            raise Exception("Файл с чатами еще не создан.") 
        with open(self.Path['chats'], 'r') as file:
            data = json.load(file)
        return data


    def loadApi(self):
        if not self.apiExists():
            raise Exception("Файл с APi еще не создан.") 
        pass

    def chatExists(self):
        return os.path.exists(self.Path['chats'])
    def apiExists(self):
        return os.path.exists(self.Path['api'])
        
    
