from telethon.sync import TelegramClient , events , Button
import logging
import sqlite3 
import hashlib
import os 
from dotenv import load_dotenv
import asyncio

# Using ./.env File
load_dotenv()

# os.getenv output is passing string var / 
# so for ApiId we must to convert it to integer
Client = TelegramClient('data' , int(os.getenv('ApiId')) , os.getenv('ApiHash') )
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

def AdminCheck(TelUserId) : 
    Cursor.execute(f'select Access from Info where TelUserId = {TelUserId}')
    Permission = Cursor.fetchone()[0]

    if Permission : 
        return True

    return False

async def JoinCheck(TelUserId) : 
    # Check if the user is a member or not / 
    # if it's not a member , get_permissions raise an error 

    try : 
        await Client.get_permissions('VortexSaver' , TelUserId) 
        return True 

    except : 
        return False 

async def AdminPanel(event) : 
    ButtonMarkup = event.client.build_reply_markup([
        [Button.text('New Admin 👨‍💼/👩‍💼') , Button.text('Channel Sponser 🚀')],
        [Button.text('Ban User 🚫') , Button.text('Users Numbers 📊')] ,
        [Button.text('Home 🏠')]
        ])

    await event.respond('Hey to our admin' , buttons = ButtonMarkup)




@Client.on(events.NewMessage(pattern = '/start' )) 
async def Start(event) : 
    
    if AdminCheck(event.message.chat_id) : 
        await AdminPanel(event)  


    # Check if user is join our channel or not  
    elif await JoinCheck(event.message.chat_id) : 
            
        if not UserExist(event.message.chat_id) :
            AddUser(event.message.chat_id) 

        
        # If telegram account is acctive 
        if ActivateCheck(event.message.chat_id) : 
            await event.respond("Hi")
                
        else : 
            await event.respond('Your account is not active .\nplease activate your account with /activate .')
    
    else : 
        JoinButton = Button.url("Vortex Saver 🌪", url='https://t.me/VortexSaver')
        await event.respond('You must join to above channels before using the bot . \n/start after join the channel . ' , buttons = [[JoinButton]])

@Client.on(events.NewMessage(pattern = '/activate' ))
async def Activate(event) :  
    # Check if user is join our channel or not  
    if await JoinCheck(event.message.chat_id) :

        if ActivateCheck(event.message.chat_id) : 
            await event.respond('You are already Activated ! ')
                
        else :
            InstaLink = 'https://www.instagram.com/' + os.getenv('InstaUsername')
            AuthKey = AuthKeyCreator(event.message.chat_id)
            await event.respond(f'Send this AuthKey to [this page]({InstaLink})\n`{AuthKey}`')
    
    else : 
        JoinButton = Button.url("Vortex Saver 🌪", url='https://t.me/VortexSaver')
        await event.respond('You must join to above channels before using the bot . \n/start after join the channel . ' , buttons = [[JoinButton]])


@Client.on(events.NewMessage(pattern = '/sendall'))
async def Broadcast(event) : 
    if AdminCheck(event.message.chat_id) : 
        Cursor.execute('select TelUserId from Info ')
        UserIds = list(map(lambda x : x[0] , Cursor.fetchall()))
        for UserId in UserIds :
            await Client.send_message(UserId , event.raw_text[8:]) 

    else : 
        await event.respond('Hi')

# These above patter need to be admin 
@Client.on(events.NewMessage(pattern = 'Channel Sponser 🚀'  , func = lambda event : AdminCheck(event.message.chat_id))) 
async def Sponser(event) : 
    ButtonMarkup = event.client.build_reply_markup([
        [Button.text('Status ℹ️')],
        [Button.text('Add 🆕') , Button.text('Remove 🚮')] , 
        [Button.text('Home 🏠')]
        ])

    await event.respond('Ok Sir , you want to Add Or Remove' , buttons = ButtonMarkup)
    




def RunBot() :
    Client.start(bot_token = os.getenv('Token'))
    print('Successfully Connected !')
    Client.run_until_disconnected()

