from utils.instagram.__init__ import Cursor 

def InstaUserId(InstaUserId , TelUserId) : 
    self.Cursor.execute(f'update Info set InstaUserId = {Message.user_id} ,\
            Active = 1 where TelUserId = {TelUserId} ')

