from app.handler import Handler
import asyncio

class Application:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.handler = Handler(self.loop)
        self.loop.run_forever()