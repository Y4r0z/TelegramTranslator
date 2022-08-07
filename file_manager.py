# -*- coding: utf-8 -*-
from data_manager import DataManager
from messages.media import Media, MediaType
import json
class FileManager:
    Path =\
    {
        'chats':'config/chats.json'
    }
    def __init__(self):
        self.data = DataManager()
        self.filesPath = 'Temp/'
    
    async def downloadTgMedia(self, event, bot_client):
        filename = event.file.name
        path = await bot_client.download_media(event.media, self.filesPath)
        return Media(filename, MediaType.FromEvent(event), path)


    
