from utils.telegram.__init__ import Cursor
from telethon.tl.types import PeerChannel

def Users() : 
    Cursor.execute('select TelUserId from Info')
    UserIds = list(map(lambda x : x[0] , Cursor.fetchall()))

    return UserIds

def Admins() : 
    Cursor.execute('select TelUserId from Info where Admin = 1')
    AdminsId = list(map(lambda x : x[0] , Cursor.fetchall()))

    return AdminsId 

async def GroupId(Client , GroupChatUsername) : 
    try : 
        GroupChatEntity = await Client.get_entity(GroupChatUsername) 
        return GroupChatEntity.id

    except : 
        return False 

def GroupTitle(Client , GroupChatId) : 
    try : 
        GroupChatEntity = await Client.get_entity(GroupChatUsername) 
        return GroupChatEntity.title

    except : 
        return False 

def Groups(TelUserId) : 
    Cursor.execute(f'select Groups from Info where TelUserId = {TelUserId}')
    Group = Cursor.fetchone()

    if Group : 
        return Group[0]

    return int(Group)
