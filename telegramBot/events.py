from telethon.sync import TelegramClient , events
import sys 
import logging
import sqlite3 
import hashlib

# add path 
sys.path.append('../')

import config


Client = TelegramClient('data' , config.ApiId , config.ApiHash )
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING) 

# Connect to DataBase
Connection = sqlite3.connect('Vortex.db' , isolation_level = None , check_same_thread = False )
Cursor = Connection.cursor()


def ActivateCheck(TelUserId) : 
    Cursor.execute(f'select Active from Info where TelUserId = {TelUserId}')
    Active = Cursor.fetchone()[0]
    return Active 

def UserExist(TelUserId) : 
    Cursor.execute(f'select TelUserId from Info')
    # Cursor.fecthall output is like this : [(1,) , (2,)]
    # with above code i convert it to this : [1,2]
    UserIdsList = list(map(lambda x : x[0] , Cursor.fetchall()))  
    return TelUserId in UserIdsList

def AddUser(TelUserId) : 
    Cursor.execute(f'insert into Info (TelUserId , Access , Active) values ({TelUserId} , 0 , 0)')

def AuthKeyCreator(TelUserId) : 
    Cursor.execute(f'select AuthKey from Info where TelUserId = {TelUserId}')
    AuthKey = Cursor.fetchone()[0]

    if not AuthKey : 
        AuthKey = 'AuthKey$' + hashlib.sha1(str(TelUserId).encode()).hexdigest()
        Cursor.execute(f'update Info set AuthKey = "{AuthKey}" where TelUserId = {TelUserId}')

    return AuthKey

@Client.on(events.NewMessage(pattern = '/start')) 
async def Start(event) : 

    if not UserExist(event.message.chat_id) :
        AddUser(event.message.chat_id) 

    
    # If telegram account is acctive 
    if ActivateCheck(event.message.chat_id) : 
        await event.respond("Hi")
    
    else : 
        await event.respond('Your account is not active .\nplease activate your account with /activate .')


@Client.on(events.NewMessage(pattern = '/activate'))
async def Activate(event) :  

    if ActivateCheck(event.message.chat_id) : 
        await event.respond('You are already Activated ! ')
            
    else :
        InstaLink = 'https://www.instagram.com/' + config.InstaUsername
        AuthKey = AuthKeyCreator(event.message.chat_id)
        await event.respond(f'Send this AuthKey to [this page]({InstaLink})\n`{AuthKey}`')







def RunBot() :
    Client.start(bot_token = config.Token)
    print('Successfully Connected !')
    Client.run_until_disconnected()

