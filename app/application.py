from app.handler import Handler
import asyncio
import logging as log
 
class Application:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.handler = Handler(self.loop)
    
    def run(self):
        self.handler.run()
    
    def exit(self):
        log.info("exit app")
        self.handler.exit()