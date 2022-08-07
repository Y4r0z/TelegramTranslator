import platforms

class ChatBot:
    Platfrom = platforms.Platform.none

    def __init__(self, handler, bot):
        self.handler = handler
        self.handler.add(self)
        self.bot = bot
    