from utils.telegram.__init__ import Cursor

def Users() : 
    Cursor.execute('select TelUserId from Info')
    UserIds = list(map(lambda x : x[0] , Cursor.fetchall()))

    return UserIds

def Admins() : 
    Cursor.execute('select TelUserId from Info where Admin = 1')
    AdminsId = list(map(lambda x : x[0] , Cursor.fetchall()))

    return AdminsId 

def GroupId(Client , GroupChatUsername) : 
    try : 
        GroupChatEntity = Client.get_entity(GroupChatUsername) 
        return GroupChatEntity.id

    except : 
        return False 
