import os
from time import sleep


class Main :

    def __init__(self): 
        ConfigCheck() 
    
        # First check for config because in instaApi we import config 
        import instaApi 

        self.Page = instaApi.InstagramAPI()
        
    def CheckDMs(self): 
        # check every second 
        while True :  
            Directs = list(self.Page.CheckPost())
            print(Directs)

            sleep(1) 




def ConfigCheck() : 
    if not os.path.exists('config.py') : 
        InstaUsername = input('Enter your Instagram Username : ')
        InstaPass = input('Enter your Instagram Password : ')
        TelNumber = input('Enter your Telegram Number ( START WITH + ) : ')
        # Writing config file 
        with open('config.py' , 'w') as File : 
            File.write(f'InstaUsername = "{InstaUsername}"')
            File.write(f'\nInstaPass = "{InstaPass}"')
            File.write(f'\nTelNumber = "{TelNumber}"')



if __name__ == '__main__' : 
    MainClass = Main()
    MainClass.CheckDMs()
