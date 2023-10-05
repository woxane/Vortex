import sqlite3

_Connection = sqlite3.connect('../database/Vortex.db' , isolation_level = None , check_same_thread = False)
Cursor = _Connection.cursor()

def MessagesEn() : 
    Messages = {
            'ActivateWarning' : 'Your Account is not Activated 🚷' ,
            }

    return Messages

def MessagesFa() : 
    Messages = {
            'ActivateWarning' : 'اکانت شما اکتیو نمیباشد 🚷' , 
            }

    return Messages
