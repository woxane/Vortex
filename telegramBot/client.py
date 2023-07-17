from telethon.sync import TelegramClient , events
import sys
import logging
import threading
import asyncio 

# add path
sys.path.append('../')
import config

sys.path.append('telegramBot/')
import events


class Bot : 

    def __init__(self) : 
        self.Client = TelegramClient('data1' , config.ApiId , config.ApiHash )

        logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                            level=logging.WARNING)
       
        EventsThread = threading.Thread(target=EventThread)
        EventsThread.daemon = True
        EventsThread.start()

        self.Client.start(bot_token = config.Token) 
    

    def SendMedia(self , Url , TelUserId , Caption) : 
        self.Client.send_file(TelUserId , Url , caption=Caption , force_document=False) 

    
    def SendMessage(self , Message , TelUserId) : 
        self.Client.send_message(TelUserId , 'Acctivated ! ')


        
def EventThread() : 
    Loop = asyncio.new_event_loop()
    asyncio.set_event_loop(Loop)

    events.RunBot()
    

