from __init__ import Cursor

def Exists(TelUserId) : 
    Cursor.execute(f'select TelUserId from Info')
    # Cursor.fecthall output is like this : [(1,) , (2,)]
    # with above code i convert it to this : [1,2]
    UserIdsList = list(map(lambda x : x[0] , Cursor.fetchall()))  
    return TelUserId in UserIdsList

def Add(TelUserId) : 
    Cursor.execute(f'insert into Info (TelUserId , Access , Active , Admin) values ({TelUserId} , 1 , 0 ,0)')
