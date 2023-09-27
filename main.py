import os
from dotenv import load_dotenv
from telegramBot import client

class Main :

    def __init__(self): 
        #Use .env file 
        load_dotenv()

        ConfigCheck() 
    
        # First check for config because in instaApi we import config 
        import instaApi 

        self.Page = instaApi.InstagramAPI()

        self.TelBot = client.Bot()
        
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
        except : 
            print('Log out...')
            print('Try to log in... ')
            self.Page.Login()
            self.CheckDms()


    def SendMedia(self , Url , TelUserId , Caption ) :
        self.TelBot.SendMedia(Url , TelUserId , Caption) 

    
    def SendMessage(self , Message , TelUserId ) :
        self.TelBot.SendMessage(Message , TelUserId)


def ConfigCheck() : 
    if not os.path.exists('.env') : 
        InstaUsername = input('Enter your Instagram Username : ')
        InstaPass = input('Enter your Instagram Password : ')
        ApiId = int(input('Enter your Telegram Bot Api Id : '))
        ApiHash = input('Enter you Telegram Bot Api Hash : ' )
        Token = input('Enter you Telegram Bot Token : ')
        # Writing config file 
        with open('.env' , 'w') as File : 
            File.write(f'InstaUsername={InstaUsername}')
            File.write(f'\nInstaPass={InstaPass}')
            File.write(f'\nApiId={ApiId}')
            File.write(f'\nApiHash={ApiHash}')
            File.write(f'\nToken={Token}')


if __name__ == '__main__' : 
    MainClass = Main()
    MainClass.CheckDMs()
