from telethon.sync import TelegramClient , events , Button
import logging
import sqlite3 
import hashlib
import os 
from dotenv import load_dotenv
import asyncio
from datetime import datetime
import json
from utils.telegram import (
        Alter , 
        ButtonMaker , 
        Check , 
        Sponsors , 
        User ,
        Find , 
        )

# Using ./.env File
load_dotenv()

# os.getenv output is passing string var / 
# so for ApiId we must to convert it to integer
Client = TelegramClient('data' , int(os.getenv('ApiId')) , os.getenv('ApiHash') )
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING) 

# Connect to DataBase
Connection = sqlite3.connect('../database/Vortex.db' , isolation_level = None , check_same_thread = False )
Cursor = Connection.cursor()


def AuthKeyCreator(TelUserId) : 
    Cursor.execute(f'select AuthKey from Info where TelUserId = {TelUserId}')
    AuthKey = Cursor.fetchone()[0]

    if not AuthKey : 
        AuthKey = 'AuthKey$' + hashlib.sha1(str(TelUserId).encode()).hexdigest()
        Cursor.execute(f'update Info set AuthKey = "{AuthKey}" where TelUserId = {TelUserId}')

    return AuthKey


async def AdminPanel(event , Message) : 
    ButtonMarkup = event.client.build_reply_markup([
        [Button.text('Send All 📢')],
        [Button.text('Admins 👨‍💼/👩‍💼') , Button.text('Channel Sponser 🚀')],
        [Button.text('Ban/UnBan User 🚫') , Button.text('Users Numbers 📊')] ,
        [Button.text('Home 🏠')]
        ])

    await event.respond(Message , buttons = ButtonMarkup)

async def GetReply(Message , TelUserId) :
    async with Client.conversation(TelUserId) as Chat : 
        await Chat.send_message(Message , buttons = Button.force_reply()) 
        
        return (await Chat.get_reply()).text

    

@Client.on(events.NewMessage(pattern = '/start' , func = lambda event : Check.Access(event.message.chat_id))) 
async def Start(event) : 
    
    if Check.Admin(event.message.chat_id) : 
        await AdminPanel(event , 'Hey Admin 🤵')  


    elif not User.Exists(event.message.chat_id) :
        User.Add(event.message.chat_id) 
        await event.respond('Please select the language you want to set 🗣' ,\
                buttons = ButtonMaker.Inline(['English 🇬🇧' ,'فارسی 🇮🇷']))
        
    # Check if user is join our channel or not  
    if Check.IsMember(Client , event.message.chat_id) : 
            
        # If telegram account is acctive 
        if Check.Active(event.message.chat_id) : 
            await event.respond("Hi")
                
        else : 
            await event.respond('Your account is not active .\nplease activate your account with /activate .')
    
    else : 
        Names , Links = zip(*(map(lambda Data : [Data['Name'] , Data['Link']] , Sponsors.Data()['Channels'])))
        UrlButtons = ButtonMaker.Url(Names , Links ,  '✅')
        await event.respond('You must join to above channels before using the bot 🚷. \nClick ✅ after join the channel . ' , buttons = UrlButtons)

@Client.on(events.NewMessage(pattern = '/activate' , func = lambda event : Check.Access(event.message.chat_id)))
async def Activate(event) :  
    # Check if user is join our channel or not  
    if Check.IsMember(Client , event.message.chat_id) :

        if Check.Active(event.message.chat_id) : 
            await event.respond('You are already Activated ! ')
                
        else :
            InstaLink = 'https://www.instagram.com/' + os.getenv('InstaUsername')
            AuthKey = AuthKeyCreator(event.message.chat_id)
            await event.respond(f'Send this AuthKey to [this page]({InstaLink})\n`{AuthKey}`')
    
    else : 
        Names , Links = zip(*(map(lambda Data : [Data['Name'] , Data['Link']] , Sponsors.Data()['Channels'])))
        UrlButtons = ButtonMaker.Url(Names , Links ,  '✅')
        await event.respond('You must join to above channels before using the bot . \nClick ✅ after join the channel . ' , buttons = UrlButtons)

@Client.on(events.NewMessage(pattern = '/feedback' , func = lambda event : Check.Access(event.message.chat_id)))
async def Feedback(event) : 
    Message = await GetReply('Send your feedback' , event.message.chat_id) 
    AdminsId = Find.Admins()
    ButtonMarkup = ButtonMaker.Inline([str(event.message.chat_id)] , Data = b'TelUserId')
    for AdminId in AdminsId : 
        await Client.send_message(AdminId , '**From User : **\n    ' + Message , buttons = ButtonMarkup)

    await event.respond('Done')

@Client.on(events.NewMessage(pattern = '/help' , func = lambda event : Check.Access(event.message.chat_id)))
async def Help(event) :
    await event.respond('''/start Welcome message
/activate Activate your account
/feedback Send a feedback to developer
/help Shows the help message''') 

@Client.on(events.NewMessage(pattern = 'Send All 📢' , func = lambda event : Check.Admin(event.message.chat_id)))
async def Broadcast(event) : 
    Message = await GetReply('Send your message ' , event.message.chat_id)
    UserIds = Find.Users()

    for UserId in UserIds :
        await Client.send_message(UserId , '**Admin Message : \n**' + Message ) 


# These above patter need to be admin 
@Client.on(events.NewMessage(pattern = 'Channel Sponser 🚀'  , func = lambda event : Check.Admin(event.message.chat_id))) 
async def Sponser(event) : 
    ButtonMarkup = event.client.build_reply_markup([
        [Button.text('Status ℹ️')],
        [Button.text('Add 🆕') , Button.text('Remove 🚮')] , 
        [Button.text('Home 🏠')]
        ])

    await event.respond('Ok Sir , you want to Add Or Remove' , buttons = ButtonMarkup)
    

@Client.on(events.NewMessage(pattern = 'Add 🆕'  , func = lambda event : Check.Admin(event.message.chat_id))) 
async def SponserAdd(event) : 

    ChannelName = await GetReply('Enter the name of the channel . ' , event.message.chat_id)
    ChannelLink = await GetReply('Enter link of the channel . ' , event.message.chat_id)
    
    Sponsors.Add(ChannelName , ChannelLink)
    
    await event.respond('Channel Successfully Added ✅')


@Client.on(events.NewMessage(pattern = 'Remove 🚮'  , func = lambda event : Check.Admin(event.message.chat_id))) 
async def SponserRemove(event) : 
    
    Data = Sponsors.Data()
    ChannelNames = list(map(lambda Channel : Channel['Name'] , Data['Channels']))

    await event.respond('Click on whichever one you want to remove 🚮' , buttons = ButtonMaker.Inline(ChannelNames , 'Done ✅'))


@Client.on(events.NewMessage(pattern = 'Status ℹ️'  , func = lambda event : Check.Admin(event.message.chat_id))) 
async def SponserStatus(event) : 
    Datas = Sponsors.Data()
    Status = list(map(lambda Channel : f'[{Channel["Name"]}]({Channel["Link"]})  :\n\
            **{Check.SpentTime(Channel["Date"])[0]} Day and {Check.SpentTime(Channel["Date"])[1]} Hours Passed**'\
            , Datas['Channels']))

    await event.respond('\n'.join(Status))

@Client.on(events.NewMessage(pattern = 'Home 🏠'  , func = lambda event : Check.Admin(event.message.chat_id))) 
async def Home(event) : 
    await AdminPanel(event , 'Back To Home 🔙') 


@Client.on(events.NewMessage(pattern = 'Users Numbers 📊'  , func = lambda event : Check.Admin(event.message.chat_id))) 
async def UserCount(event) : 
    Cursor.execute('select count(*) from Info') 
    UserCount = Cursor.fetchone()[0]
    await event.respond(f"We've Had **{UserCount}** Users Until Now")


@Client.on(events.NewMessage(pattern = 'Ban/UnBan User 🚫'  , func = lambda event : Check.Admin(event.message.chat_id))) 
async def UserAccess(event) : 
    global TelUserId
    TelUserId = await GetReply('Type the User Id ' , event.message.chat_id)
    
    if User.Exists(int(TelUserId)) :
        Access = 'Not Banned 🔓' if Check.Access(int(TelUserId)) else 'Banned 🔒' 
         
        await event.respond(f'**{TelUserId} Is {Access}**' , buttons = ButtonMaker.Inline(['Ban 🔒 / UnBan 🔓'] , 'Done ✅'))

    else : 
        await event.respond('Not Found 🔍')


@Client.on(events.NewMessage(pattern = 'Admins 👨‍💼/👩‍💼' , func = lambda event : Check.Admin(event.message.chat_id))) 
async def Admins(event) : 
    global TelUserId
    TelUserId = await GetReply('Type the User Id ' , event.message.chat_id)
    
    if User.Exists(int(TelUserId)) :
        Permission = 'Admin 👨‍💼' if Check.Admin(int(TelUserId)) else 'not Admin 👷'

        await event.respond(f'**{TelUserId} is {Permission}**' , buttons = ButtonMaker.Inline(['Grant 👨‍💼 / Revoke 👷 Admin'] , 'Done ✅'))

    else : 
        await event.respond('Not Found 🔍')


@Client.on(events.CallbackQuery())
async def InlineRemove(event) :
    DataSelection = event.data.decode()
    InlineMessage = await event.get_message()
    UserIdSelection = InlineMessage.buttons[0][0].text

    ChannelNames = list(map(lambda Channel : Channel['Name'] , Sponsors.Data()['Channels']))

    if DataSelection in ChannelNames : 
        # delete and pass the data
        ChannelNames = Sponsors.Remove(DataSelection)  
        await event.answer('Removed ❌') 
        await event.edit('Click on whichever one you want to remove 🚮' , buttons = ButtonMaker.Inline(ChannelNames , 'Done ✅'))
   
    elif DataSelection == 'Ban 🔒 / UnBan 🔓' : 
        Access = 0 if Check.Access(TelUserId) else 1
        Alter.Access(TelUserId , Access) 
        Access = 'Not Banned 🔓' if Access else 'Banned 🔒' 

        await event.edit(f'**{TelUserId} Is {Access}**' , buttons = ButtonMaker.Inline(['Ban 🔒 / UnBan 🔓'] , 'Done ✅'))
    
    elif DataSelection == 'Grant 👨‍💼 / Revoke 👷 Admin' : 
        Permission = 0 if Check.Admin(TelUserId) else 1 
        Alter.Admin(TelUserId , Permission)
        Permission = 'Admin 👨‍💼' if Check.Admin(int(TelUserId)) else 'not Admin 👷'

        await event.edit(f'**{TelUserId} is {Permission}**' , buttons = ButtonMaker.Inline(['Grant 👨‍💼 / Revoke 👷 Admin']  , 'Done ✅'))

    # Done ✅ is specially for something for admins 
    elif DataSelection == 'Done ✅' : 
        await event.edit('Successfully Completed 🫡')


    # ✅ is specially for something for users  
    elif DataSelection == '✅' :
        if Check.IsMember(Client , event.query.user_id) :  
            await event.edit('Successfully Completed 🫡')

        else : 
            await event.answer("🚷 You haven't joined all the channels 🚷")
    
    elif DataSelection == 'TelUserId' : 
        await InlineMessage.delete() 
        Message = await GetReply(f'Send your message to {UserIdSelection}' , event.query.user_id)
        await Client.send_message(int(UserIdSelection) , f'**Your answer from developer : **\n    ' + Message )

    # Change it later
    else : 
        await event.edit('❌❌❌ There is Bug if you see it please dm me ❌❌❌')
         




def RunBot() :
    Client.start(bot_token = os.getenv('Token'))
    print('Successfully Connected !')
    Client.run_until_disconnected()
    
