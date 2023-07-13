from instagrapi import Client
import config
import sqlite3


class InstagramAPI :

    def __init__(self) : 

        # Initialize Arrays
        self.Username = config.InstaUsername
        self.Password = config.InstaPass 
        
        # Login
        self.User = Client()
        self.User.login(self.Username , self.Password )
        print('Login successful!')

        # Connect to Database 
        Connection = sqlite3.connect('Vortex.db' , isolation_level = None , check_same_thread = False)
        self.Cursor = Connection.cursor()

    def CheckPost(self) : 
        UnreadDirects = self.User.direct_threads(selected_filter = 'unread')

        for Direct in UnreadDirects :  
            Message = Direct.messages[0]
            # if the last post in DM is Video  :
            if Message.item_type == 'clip' :

                self.User.direct_send('Done !' , user_ids = [Message.user_id])
                # give the data like this ( user_id , url ) for authintication we need ... 
                yield (Direct.id , ''.join(Message.clip.video_url))
            
            
            # seen the Direct for not consider the direct again
            self.User.direct_send_seen(thread_id = Direct.id)

    def PendingCheck(self) : 
        PendingDirects = self.User.direct_pending_inbox()
        
        for Direct in PendingDirects : 
            Message = Direct.messages[0]
            
            if Message.item_type == 'text' : 
                # Check if the text is AuthKey 
                # If the AuthKey was invalid don't seen it 
                TelUserId = self.AuthKeyCheck(Message)
                # Here instead of True or False we get Telegram User Id from AuthKeyCheck function 
                # and check it if it is empty or not 
                if TelUserId :  
                    self.User.direct_send('Activated' , user_ids = [Message.user_id])
                    yield TelUserId 

    def AuthKeyCheck(self , Message ) : 
        self.Cursor.execute('select TelUserId , AuthKey from Info where AuthKey is not NULL') 
        TelUserIds , AuthKeys = zip(*self.Cursor.fetchall())
         
        # Check if the AuthKey is correct 
        if Message.text in AuthKeys :
            TelUserId = TelUserIds[AuthKeys.index(Message.text)]
            self.Cursor.execute(f'update Info set InstaUserId = {Message.user_id} where TelUserId = {TelUserId} ')
            return TelUserId


    

