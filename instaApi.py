from instagrapi import Client
import config



class InstagramAPI :

    def __init__(self) : 

        # Initialize Arrays
        self.Username = config.InstaUsername
        self.Password = config.InstaPass 
        
        # Login
        self.User = Client()
        self.User.login(self.Username , self.Password )


Page = InstagramAPI

