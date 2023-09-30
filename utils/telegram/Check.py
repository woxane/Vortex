from __init__ import Cursor 
from datetime import datetime

def Admin(TelUserId) : 
    Cursor.execute(f'select Admin from Info where TelUserId = {TelUserId}')
    Permission = Cursor.fetchone()
    
    if Permission : 
        return bool(Permission[0])

    return bool(Permission)

def Access(TelUserId) : 
    Cursor.execute(f'select Access from Info where TelUserId = {TelUserId}')
    Access = Cursor.fetchone()[0]

    return bool(Access)

def SpentTime(Time) : 
    Now = datetime.now()  
    
    Days = (Now - datetime.fromisoformat(Time)).days
    Hours = (Now - datetime.fromisoformat(Time)).seconds // 3600

    return Days , Hours
