from telethon.sync import TelegramClient , events
import logging
import os 
from dotenv import load_dotenv


class Bot : 

    def __init__(self) : 
        # Using ./.env File
        load_dotenv()
            
        # os.getenv ouput is passing string var /
        # so for ApiId we must to convert it to integer
        self.Client = TelegramClient('.data' , int(os.getenv('ApiId')) , os.getenv('ApiHash') )


        logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                            level=logging.WARNING)
    

    def SendMedia(self , Url , TelUserId , Caption) : 
        self.Client.send_file(TelUserId , Url , caption=Caption , force_document=False) 

    
    def SendMessage(self , Message , TelUserId) : 
        self.Client.send_message(TelUserId , Message)


        
    

