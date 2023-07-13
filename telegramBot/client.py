from telethon.sync import TelegramClient , events
import sys
import logging

# add path
sys.path.append('../')

import config




class Bot : 

    def __init__(self) : 
        self.Client = TelegramClient('data' , config.ApiId , config.ApiHash )

        logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                            level=logging.WARNING)

        self.Client.start(bot_token = config.Token) 
        self.Client.run_until_disconnected()




