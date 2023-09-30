from telethon.sync import TelegramClient , events
import logging
import threading
import asyncio 
import os 
from dotenv import load_dotenv
from . import events


class Bot : 

    def __init__(self) : 
        # Using ./.env File
        load_dotenv()
            
        # os.getenv ouput is passing string var /
        # so for ApiId we must to convert it to integer
        self.Client = TelegramClient('data1' , int(os.getenv('ApiId')) , os.getenv('ApiHash') )


        logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                            level=logging.WARNING)
       
        EventsThread = threading.Thread(target=EventThread)
        EventsThread.daemon = True
        EventsThread.start()

        self.Client.start(bot_token = os.getenv('Token')) 
    

    def SendMedia(self , Url , TelUserId , Caption) : 
        self.Client.send_file(TelUserId , Url , caption=Caption , force_document=False) 

    
    def SendMessage(self , Message , TelUserId) : 
        self.Client.send_message(TelUserId , Message)


        
def EventThread() : 
    Loop = asyncio.new_event_loop()
    asyncio.set_event_loop(Loop)

    events.RunBot()
    

