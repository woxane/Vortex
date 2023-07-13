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
        ApiId = int(input('Enter your Telegram Bot Api Id : '))
        ApiHash = input('Enter you Telegram Bot Api Hash : ' )
        Token = input('Enter you Telegram Bot Token : ')
        # Writing config file 
        with open('config.py' , 'w') as File : 
            File.write(f'InstaUsername = "{InstaUsername}"')
            File.write(f'\nInstaPass = "{InstaPass}"')
            File.write(f'\nApiId = "{ApiId}"')
            File.write(f'\nApiHash = "{ApiHash}"')
            File.write(f'\nToken = "{Token}"')


if __name__ == '__main__' : 
    MainClass = Main()
    MainClass.CheckDMs()
