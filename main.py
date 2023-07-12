import os
import instaApi
from time import sleep


class Main :

    def __init__(self): 
        ConfigCheck() 
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
        # Writing config file 
        with open('config.py' , 'w') as File : 
            File.write(f'InstaUsername = "{InstaUsername}"')
            File.write(f'\nInstaPass = "{InstaPass}"')




if __name__ == '__main__' : 
    MainClass = Main()
    MainClass.CheckDMs()
