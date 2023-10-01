from instagrapi import Client
import sqlite3
import os 
from utils.instagram import (
        Check , 
        Alter , 
        Find , 
        )

class InstagramAPI :

    def __init__(self) : 

        ## Initialize Arrays
        self.Username = os.getenv('InstaUsername')
        self.Password = os.getenv('InstaPass')
        
        # 1 means Login Normally 
        # 0 means Login with dump.json
        self.LoginStatus = None

        self.Login()

    def Login(self) : 
        self.User = Client() 

        if os.path.exists('../database/dump.json') : 
            self.User.load_settings('../database/dump.json') 
            print('Login With dump.json')
            self.LoginStatus = 0 

        else : 
            self.User.login(self.Username, self.Password)
            self.User.dump_settings('../database/dump.json')
            print('Login Normally')
            self.LoginStatus = 1


    def CheckPost(self) : 
        UnreadDirects = self.User.direct_threads(selected_filter = 'unread')

        for Direct in UnreadDirects :  
            Message = Direct.messages[0]
            print(Message.user_id)

            if Check.Active(Message.user_id): 
                # if the last post in DM is Video  :
                if Message.item_type == 'clip' :
                        # give the data like this ( user_id , url , caption) \
                                # for authintication we need ... 
                        yield (TelUserId[0] , ''.join(Message.clip.video_url) ,\
                                Message.clip.caption_text )
           

                elif Message.item_type == 'xma_media_share' : 
                    VideoUrl = ''.join(Message.xma_share.video_url)
                    VideoPk = self.User.media_pk_from_url(VideoUrl)
                    VideoInfo = self.User.media_info(VideoPk)
                    Caption = VideoInfo.caption_text
                    for Slide in VideoInfo.resources : 
                        # If the slide is photo 
                        Type = Slide.media_type 
                        if Type == 1 :  
                            yield (TelUserId[0] , ''.join(Slide.thumbnail_url),  Caption)

                        elif Type == 2 : 
                            yield (TelUserId[0] , ''.join(Slide.video_url) , Caption) 

                
                self.User.direct_send('Done !' , user_ids = [Message.user_id])

            else : 
                self.User.direct_send('Your Account is not Activated !!' , user_ids = [Message.user_id])

            # seen the Direct for not consider the direct again
            self.User.direct_send_seen(thread_id = Direct.id)

    def PendingCheck(self) : 
        PendingDirects = self.User.direct_pending_inbox()
        
        for Direct in PendingDirects : 
            Message = Direct.messages[0]
            
            if Message.item_type == 'text' : 
                # Check if the text is AuthKey 
                # If the AuthKey was invalid don't seen it  / 
                # thats because if anyone send invalid AuthKey / 
                # could send it again cause this function / 
                # just see those pending direct for auth key 
                if Check.AuthKey(Message.user_id) : 
                    TelUserId = Find.TelUserId(Message.user_id)
                    Alter.InstaUserId(Message.user_id , TelUserId)

                    self.User.direct_send('Activated' , user_ids = [Message.user_id])
                    yield TelUserId 


    
    

