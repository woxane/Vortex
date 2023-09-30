import os
from dotenv import load_dotenv
import json
import asyncio
import threading

#XXX do something about this i don't want it like this : 
from sys import path
path.append('../')
from utils.telegram import client
from utils.instagram import instaApi
from handlers import events

class Main :

    def __init__(self): 
        #Use .env file 
        load_dotenv()

        ConfigCheck() 

        self.Page = instaApi.InstagramAPI()
        
        self.TelBot = client.Bot()
        
        EventsThread = threading.Thread(target=EventsHandler)
        EventsThread.daemon = True
        EventsThread.start()

    def CheckDMs(self): 
        # Check every second 
        try : 
            while True :  
                # Direct Check
                Directs = list(self.Page.CheckPost())
                
                # Check that Directs won't be empty
                if Directs :  
                    for Direct in Directs : 
                        # Direct[1] is Url , Shema of Direct : (id , url , caption) 
                        self.SendMedia(Direct[1] ,Direct[0] , Direct[2]) 
               
                # Check Pendings 
                ActiveTelUserIds= list(self.Page.PendingCheck()) 
                if ActiveTelUserIds: 
                    for TelUserId in ActiveTelUserIds : 
                        self.SendMessage('Activated :)' , TelUserId  ) 

        except Exception as ERROR : 
            print(f'ERROR : {ERROR}')
            print('Log out...')
            print('Try to log in... ') 
            # delete the dump.json if we login with it and failed 
            # 1 means Login Normally 
            # 0 means Login with dump.json
            if not self.Page.LoginStatus : 
                os.remove('../database/dump.json')

            self.Page.Login()
            self.CheckDMs()


    def SendMedia(self , Url , TelUserId , Caption ) :
        self.TelBot.SendMedia(Url , TelUserId , Caption) 

    
    def SendMessage(self , Message , TelUserId ) :
        self.TelBot.SendMessage(Message , TelUserId)


def ConfigCheck() : 
    if not os.path.exists('../.env') :  
        print('There is not any .env File Ready to create ...')
        InstaUsername = input('Enter your Instagram Username : ')
        InstaPass = input('Enter your Instagram Password : ')
        ApiId = int(input('Enter your Telegram Bot Api Id : '))
        ApiHash = input('Enter you Telegram Bot Api Hash : ' )
        Token = input('Enter you Telegram Bot Token : ')
        # Writing config file 
        with open('../.env' , 'w') as File : 
            File.write(f'InstaUsername={InstaUsername}')
            File.write(f'\nInstaPass={InstaPass}')
            File.write(f'\nApiId={ApiId}')
            File.write(f'\nApiHash={ApiHash}')
            File.write(f'\nToken={Token}')

        print('Done')

    if not os.path.exists('../database/SponsorsData.json') :
        print('There is not any SponsorsData.json File Ready to create ... ')
        # Creating empy json file 
        with open('../database/SponsorsData.json' , 'w') as File : 
            json.dump({'Channels' : []} , File , indent = 4)
        
        print('Done')

def EventsHandler() : 
    Loop = asyncio.new_event_loop()
    asyncio.set_event_loop(Loop)

    events.RunBot()

if __name__ == '__main__' : 
    MainClass = Main()
    MainClass.CheckDMs()
