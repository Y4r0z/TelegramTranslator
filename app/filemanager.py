import json
import os

class FileManager:
    def __init__(self):
        self.dataPath = './data/'
        self.chatsPath = self.dataPath + "chats.json"

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
        
