from utils.instagram.__init__ import Cursor

def TelUserId(InstaUserId) :
    Cursor.execute(f'select TelUserId from Info where InstaUserId = {InstaUserId}') 
    TelUserId = Cursor.fetchone()

    if TelUserId :
        return TelUserId[0]
    return TelUserId

def InstaUserId(TelUserId) :
    Cursor.execute(f'select InstaUserId from Info where TelUserId = {TelUserId}') 
    InstaUserId= Cursor.fetchone()

    if InstaUserId :
        return InstaUserId[0]
    return InstaUserId
