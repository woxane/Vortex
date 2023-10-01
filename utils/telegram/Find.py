from utils.telegram.__init__ import Cursor

def TelUserIds() : 
    Cursor.execute('select TelUserIds from Info')
    UserIds = list(map(lambda x : x[0] , Cursor.fetchall()))

    return UserIds

