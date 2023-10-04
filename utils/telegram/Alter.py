from utils.telegram.__init__ import Cursor 

def Access(TelUserId , Access) : 
    Cursor.execute(f'update Info set Access = {Access} where TelUserId = {TelUserId}')

def Admin(TelUserId , Permission) : 
    Cursor.execute(f'update Info set Admin = {Permission} where TelUserId = {TelUserId}')

def Language(TelUserId , _lang) : 
    Cursor.execute(f"update Info set Language = '{_lang}' where TelUserId = {TelUserId}")

def Group(TelUserId , GroupChatId) : 
    Cursor.execute(f'update Info set Groups = {GroupChatId} where TelUserId = {TelUserId}')
