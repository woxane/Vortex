from utils.telegram.__init__ import Cursor 
from utils.telegram import Sponsors 
from datetime import datetime

def Admin(TelUserId) : 
    Cursor.execute(f'select Admin from Info where TelUserId = {TelUserId}')
    Permission = Cursor.fetchone()
    
    if Permission : 
        return bool(Permission[0])

    return bool(Permission)

def Access(TelUserId) : 
    Cursor.execute(f'select Access from Info where TelUserId = {TelUserId}')
    Access = Cursor.fetchone()

    if Access : 
        return bool(Access[0])

    return bool(Access)

def Active(TelUserId) : 
    Cursor.execute(f'select Active from Info where TelUserId = {TelUserId}')
    Active = Cursor.fetchone()
    
    if Active : 
        return bool(Active[0])

    return bool(Active)

def SpentTime(Time) : 
    Now = datetime.now()  
    
    Days = (Now - datetime.fromisoformat(Time)).days
    Hours = (Now - datetime.fromisoformat(Time)).seconds // 3600

    return Days , Hours

async def IsMember(Client , TelUserId) : 
    # Check if the user is a member or not \
            # if it's not a member , get_permissions raise an error 

    try : 
        ChannelsLink = list(map(lambda Channel : Channel['Link'] , Sponsors.Data()['Channels']))
        for Link in ChannelsLink : 
            await Client.get_permissions(Link , TelUserId )
        return True 

    except : 
        return False

def Language(TelUserId) : 
    Cursor.execute(f'select Language from Info where TeLuserId = {TelUserId}')
    _Language = Cursor.fetchone()[0]
    return _Language

async def BotMembership(Client , GroupChat) : 
    try : 
        await Client.get_entity(GroupChat) 
        return True

    except : 
        return False
