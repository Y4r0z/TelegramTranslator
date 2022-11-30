import json
import os
from app.structs.message import Message
from telegram import PhotoSize, Sticker, Video, Voice, VideoNote, Audio, Document, Animation
from telegram import Message as TgMessage
import time

class FileManager:
    def __init__(self):
        self.dataPath = './data/'
        self.chatsPath = self.dataPath + "chats.json"
        self.filesPath = './temp/'

        if not os.path.exists(self.filesPath):
            os.makedirs(self.filesPath)

        if not os.path.exists(self.dataPath):
            os.makedirs(self.dataPath)
        
        if not os.path.exists(self.chatsPath):
            with open(self.chatsPath, 'w') as file:
                file.write('[]')

    def loadChats(self):
        with open(self.chatsPath, 'r') as file:
            data = json.load(file)
        return data

    def saveChats(self, chats):
        data = [i.json() for i in chats]
        with open(self.chatsPath, 'w') as file:
            json.dump(data, file)
    
    async def saveMedia(self, message : Message):
        mes = message.media
        if not mes.effective_attachment:
            return None
        attach = mes.effective_attachment
        if mes.photo:
            attach = attach[-1]
        if hasattr(attach, 'file_name') and attach.file_name is not None:
            name = attach.file_name
        else:
            name = 'file_' + str(int(time.time()))
        f = await attach.get_file()
        ext = "." + f.file_path.split('.')[-1]
        if ext in name:
            ext = ''
        path = self.filesPath + name + ext
        await f.download_to_drive(path)
        return path
