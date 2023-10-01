from utils.telegram.__init__ import Cursor

def Users() : 
    Cursor.execute('select TelUserIds from Info')
    UserIds = list(map(lambda x : x[0] , Cursor.fetchall()))

    return UserIds

