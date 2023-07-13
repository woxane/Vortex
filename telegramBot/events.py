from telethon.sync import TelegramClient , events
import sys 
import logging

# add path 
sys.path.append('../')

import config


Client = TelegramClient('data' , config.ApiId , config.ApiHash )
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING) 



@Client.on(events.NewMessage(pattern = '/start')) 
async def Start(event) :  
    await event.respond("Hi")











Client.start(bot_token = config.Token)
Client.run_until_disconnected()
