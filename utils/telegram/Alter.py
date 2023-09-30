from utils.telegram.__init__ import Cursor 

def Access(TelUserId , Access) : 
    Cursor.execute(f'update Info set Access = {Access} where TelUserId = {TelUserId}')

def Admin(TelUserId , Permission) : 
    Cursor.execute(f'update Info set Admin = {Permission} where TelUserId = {TelUserId}')
