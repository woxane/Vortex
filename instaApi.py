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
        
    def CheckPost(self) : 
        UnreadDirects = self.User.direct_threads(selected_filter = 'unread')

        for Direct in UnreadDirects : 
            # if the last post in DM is Video  :
            if Direct.messages[0].item_type == 'clip' :
                # seen the Direct for not consider the direct again
                self.User.direct_send_seen(thread_id = Direct.id)
                # give the data like this ( user_id , url ) for authintication we need ... 
                yield (Direct.id , ''.join(Direct.messages[0].clip.video_url))



Page = InstagramAPI()
print(list(Page.CheckPost()))
