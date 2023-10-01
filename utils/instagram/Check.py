from utils.instagram.__init__ imoprt Cursor

def Active(InstaUserId) : 
    Cursor.execute(f'select Active from Info where InstaUserId = {InstaUserId}')
    Active = Cursor.fetchone()
    
    if Active : 
        return bool(Active[0])

    return bool(Active)
