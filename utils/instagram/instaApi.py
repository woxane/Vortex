from instagrapi import Client
import sqlite3
import os 
from utils.instagram import (
        Check , 
        Alter , 
        Find , 
        )
from utils.instagram.__init__ import *
from utils.telegram.Check import Language
from requests import Session

class InstagramAPI :

    def __init__(self , Proxy = None) : 

        ## Initialize Arrays
        self.Username = os.getenv('InstaUsername')
        self.Password = os.getenv('InstaPass')
        
        # 1 means Login Normally 
        # 0 means Login with dump.json
        self.LoginStatus = None

        self.Login(Proxy)

    def Login(self , Proxy = None) : 
        self.User = Client()
        if Proxy : 
            Session_ = Session()
            Session_.proxies = {'http' : Proxy , 'https' : Proxy}
            self.User.session = Session_

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

            TelUserId = Find.TelUserId(Message.user_id)
            if Check.Active(Message.user_id): 
                # if the last post in DM is Video  :
                if Message.item_type == 'clip' :
                        # give the data like this ( user_id , url , caption) \
                                # for authintication we need ... 
                        yield (TelUserId , ''.join(Message.clip.video_url) ,\
                                Message.clip.caption_text )
           

                elif Message.item_type == 'xma_media_share' : 
                    VideoUrl = ''.join(Message.xma_share.video_url)
                    VideoPk = self.User.media_pk_from_url(VideoUrl)
                    VideoInfo = self.User.media_info(VideoPk)
                    Caption = VideoInfo.caption_text
                    if VideoInfo.resources : 
                        for Slide in VideoInfo.resources : 
                            # If the slide is photo 
                            Type = Slide.media_type 
                            if Type == 1 :  
                                yield (TelUserId , ''.join(Slide.thumbnail_url),  Caption)

                            elif Type == 2 : 
                                yield (TelUserId , ''.join(Slide.video_url) , Caption) 
                    else : 
                        yield (TelUserId , ''.join(VideoInfo.thumbnail_url) , Caption)


                #XXX THIS ABOVE CODE WON'T WORK ON NORMAL INSTAGRAPI LIBRARY
                # I CHANGE A LITTLE CODE , FOR GETTING THE STORYS
                elif Message.item_type ==  'xma_story_share' : 
                    print(Message)
                    StoryUrl = ''.join(Message.xma_share.preview_url)
                    yield (TelUserId , StoryUrl , '')


            else :

                if Language(TelUserId) == 'en' : 
                    Messages = MessagesEn()
                elif Language(TelUserId) == 'fa' : 
                    Messages = MessagesFa()

                self.SendMessage(Messages['ActivateWarning'] , Message.user_id)

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
                if Check.AuthKey(Message.text) : 
                    TelUserId = Find.TelUserId(Message.user_id)
                    Alter.InstaUserId(Message.user_id , TelUserId)

                    self.User.direct_send('Activated' , user_ids = [Message.user_id])
                    yield TelUserId 

    def SendMessage(self , Message , InstaUserId) :
        self.User.direct_send(Message , user_ids = [InstaUserId])
    
    

