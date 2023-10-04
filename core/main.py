import os
from dotenv import load_dotenv
import json
import asyncio
import threading

#XXX do something about this i don't want it like this : 
from sys import path , argv 
path.append('../')
from utils.telegram import client , Check
from utils.instagram import instaApi , Find
from utils.general import Config , ValidationCheck , Flag
from handlers import events
from instagrapi.exceptions import LoginRequired

class Main :

    def __init__(self): 
        #Use .env file 
        load_dotenv()

        ConfigCheck() 
        
        if len(argv) > 1 :
            Flag.Check(argv[1])  

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
                        if asyncio.run(Check.IsMember(self.TelBot.Client , Direct[0])) :  
                            self.SendMedia(Direct[1] ,Direct[0] , Direct[2])
                        else : 
                            self.SendMessage("You Can't Access the bot until you joined the Sponsors Channel" , Direct[0])
                            InstaUserId = Find.InstaUserId(Direct[0])
                            self.Page.SendMessage("You Can't Access the bot until you joined the Sponsors Channel" , InstaUserId)
                               
               
                # Check Pendings 
                ActiveTelUserIds= list(self.Page.PendingCheck()) 
                if ActiveTelUserIds: 
                    for TelUserId in ActiveTelUserIds : 
                        self.SendMessage('Activated :)' , TelUserId  ) 

        except LoginRequired as ERROR : 
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
        Config.CreateEnv('../.env')
        print('Done')

    if not os.path.exists('../database/SponsorsData.json') :
        print('There is not any SponsorsData.json File Ready to create ... ')
        Config.CreateJson('../database/SponsorsData.json' , {'Channels' : []})
        print('Done')
    
    if not ValidationCheck.JsonFile('../database/SponsorsData.json') : 
        print('The SponsorsData.json is corrupted ...')
        input('Enter to continue Creating New SponsorsData.json file ...')
        Config.CreateJson('../database/SponsorsData.json' , {'Channels' : []})

    if not ValidationCheck.Env('../.env') :
        print('The .env is corrupted ...')
        input('Enter to continue Creating New .env file ...')
        Config.CreateEnv('../.env')


def EventsHandler() : 
    Loop = asyncio.new_event_loop()
    asyncio.set_event_loop(Loop)

    events.RunBot()

if __name__ == '__main__' : 
    MainClass = Main()
    MainClass.CheckDMs()
