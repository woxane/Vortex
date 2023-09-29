from telethon.sync import TelegramClient , events , Button
import logging
import sqlite3 
import hashlib
import os 
from dotenv import load_dotenv
import asyncio
from datetime import datetime
import json

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
    Cursor.execute(f'insert into Info (TelUserId , Access , Active , Admin) values ({TelUserId} , 1 , 0 ,0)')

def AuthKeyCreator(TelUserId) : 
    Cursor.execute(f'select AuthKey from Info where TelUserId = {TelUserId}')
    AuthKey = Cursor.fetchone()[0]

    if not AuthKey : 
        AuthKey = 'AuthKey$' + hashlib.sha1(str(TelUserId).encode()).hexdigest()
        Cursor.execute(f'update Info set AuthKey = "{AuthKey}" where TelUserId = {TelUserId}')

    return AuthKey

def AdminCheck(TelUserId) : 
    Cursor.execute(f'select Admin from Info where TelUserId = {TelUserId}')
    Permission = Cursor.fetchone()[0]

    if Permission : 
        return True

    return False

def ButtonMaker(DataList , ButtonType) :
    # i want to inline buttons seprate two by two for this : 
    
    Buttons = list(map(lambda DataIndex : [ButtonType(DataList[DataIndex]) , ButtonType(DataList[DataIndex + 1])] \
            if DataIndex + 1 != len(DataList) else [ButtonType(DataList[DataIndex])] ,\
            range(len(DataList))[::2] ))
   
    # this is for i want the done button be big and seprated
    Buttons.append([Button.inline('Done ✅')])

    return Buttons

def SponsersData() : 
    with open('SponsersData.json' , 'r') as File : 
        Datas = json.load(File)

    return Datas

def SponserRemover(Name) :  
    Datas = SponsersData()
    Datas = {'Channels' : list(filter(lambda Channels : Channels['Name'] != Name , Datas['Channels']))}

    with open('SponsersData.json' , 'w' ) as File : 
        json.dump(Datas , File , indent = 4)
    
    return list(map(lambda Channels : Channels['Name'] , Datas['Channels']))

async def JoinCheck(TelUserId) : 
    # Check if the user is a member or not / 
    # if it's not a member , get_permissions raise an error 

    try : 
        ChannelsLink = list(map(lambda Channel : Channel['Link'] , SponsersData()))
        for Link in ChannelsLink : 
            await Client.get_permissions(Link , TelUserId )
        return True 

    except : 
        return False 

async def AdminPanel(event , Message) : 
    ButtonMarkup = event.client.build_reply_markup([
        [Button.text('Send All 📢')],
        [Button.text('New Admin 👨‍💼/👩‍💼') , Button.text('Channel Sponser 🚀')],
        [Button.text('Ban/UnBan User 🚫') , Button.text('Users Numbers 📊')] ,
        [Button.text('Home 🏠')]
        ])

    await event.respond(Message , buttons = ButtonMarkup)

async def GetReply(Message , TelUserId) :
    async with Client.conversation(TelUserId) as Chat : 
        await Chat.send_message(Message , buttons = Button.force_reply()) 
        
        return (await Chat.get_reply()).text

    

@Client.on(events.NewMessage(pattern = '/start' )) 
async def Start(event) : 
    
    if AdminCheck(event.message.chat_id) : 
        await AdminPanel(event , 'Hey Admin 🤵')  


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
        ChannelsLink = list(map(lambda Channel : Channel['Link'] , SponsersData()['Channels']))
        UrlButtons = ButtonMaker(ChannelsLink , Button.url)
        await event.respond('You must join to above channels before using the bot . \n/start after join the channel . ' , buttons = UrlButtons)

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
        ChannelsLink = list(map(lambda Channel : Channel['Link'] , SponsersData()['Channels']))
        UrlButtons = ButtonMaker(ChannelsLink , Button.url)
        await event.respond('You must join to above channels before using the bot . \n/start after join the channel . ' , buttons = UrlButtons)


@Client.on(events.NewMessage(pattern = 'Send All 📢' , func = lambda event : AdminCheck(event.message.chat_id)))
async def Broadcast(event) : 
    Message = await GetReply('Send your message ' , event.message.chat_id)

    Cursor.execute('select TelUserId from Info ')
    UserIds = list(map(lambda x : x[0] , Cursor.fetchall()))
    for UserId in UserIds :
        await Client.send_message(UserId , '**Admin Message : \n**' + Message ) 


# These above patter need to be admin 
@Client.on(events.NewMessage(pattern = 'Channel Sponser 🚀'  , func = lambda event : AdminCheck(event.message.chat_id))) 
async def Sponser(event) : 
    ButtonMarkup = event.client.build_reply_markup([
        [Button.text('Status ℹ️')],
        [Button.text('Add 🆕') , Button.text('Remove 🚮')] , 
        [Button.text('Home 🏠')]
        ])

    await event.respond('Ok Sir , you want to Add Or Remove' , buttons = ButtonMarkup)
    

@Client.on(events.NewMessage(pattern = 'Add 🆕'  , func = lambda event : AdminCheck(event.message.chat_id))) 
async def SponserAdd(event) : 

    ChannelName = await GetReply('Enter the name of the channel . ' , event.message.chat_id)
    ChannelLink = await GetReply('Enter link of the channel . ' , event.message.chat_id)
   
    Data = SponsersData()
    
    Data['Channels'].append({'Name' : ChannelName , 'Link' : ChannelLink , 'Date' : datetime.now().isoformat()})
    
    with open('SponsersData.json' , 'w') as File : 
        json.dump(Data  , File , indent = 4)

    await event.respond('Channel Successfully Added ✅')


@Client.on(events.NewMessage(pattern = 'Remove 🚮'  , func = lambda event : AdminCheck(event.message.chat_id))) 
async def SponserRemove(event) : 
    # Global is the bad idea change it next time
    global ChannelNames
    
    Data = SponsersData()
    ChannelNames = list(map(lambda Channel : Channel['Name'] , Data['Channels']))

    await event.respond('Click on whichever one you want to remove 🚮' , buttons = ButtonMaker(ChannelNames , Button.inline))


@Client.on(events.NewMessage(pattern = 'Status ℹ️'  , func = lambda event : AdminCheck(event.message.chat_id))) 
async def SponserStatus(event) : 
    Datas = SponsersData()
    Now = datetime.now()  
    Status = list(map(lambda Channel : f'[{Channel["Name"]}]({Channel["Link"]})  :\n\
            **{(Now - datetime.fromisoformat(Channel["Date"])).days} Day and {(Now - datetime.fromisoformat(Channel["Date"])).seconds // 3600} Hours Passed**'\
            , Datas['Channels']))

    await event.respond('\n'.join(Status))

@Client.on(events.NewMessage(pattern = 'Home 🏠'  , func = lambda event : AdminCheck(event.message.chat_id))) 
async def Home(event) : 
    await AdminPanel(event , 'Back To Home 🔙') 


@Client.on(events.NewMessage(pattern = 'Users Numbers 📊'  , func = lambda event : AdminCheck(event.message.chat_id))) 
async def UserCount(event) : 
    Cursor.execute('select count(*) from Info') 
    UserCount = Cursor.fetchone()[0]
    await event.respond(f"We've Had **{UserCount}** Users Until Now")


@Client.on(events.CallbackQuery())
async def InlineRemove(event) :
    global ChannelNames
    UserSelection = event.data.decode()
    
    if UserSelection in ChannelNames : 
        # delete and pass the data
        ChannelNames = SponserRemover(UserSelection)  
        await event.answer('Removed ❌') 
        await event.edit('Click on whichever one you want to remove 🚮' , buttons = ButtonMaker(ChannelNames , Button.inline))
    
    # none of them means it's Done 
    else : 
        await event.edit('Successfully Completed 🫡')
         




def RunBot() :
    Client.start(bot_token = os.getenv('Token'))
    print('Successfully Connected !')
    Client.run_until_disconnected()
    
