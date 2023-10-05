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
from handlers.__init__ import *

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


async def BanWarning(event) : 
    if Check.Language(event.message.chat_id) == 'en' : 
        Message = BanEn()

    elif Check.Language(event.message.chat_id) == 'fa' : 
        Message = BanFa() 

    await event.respond(Message)

@Client.on(events.NewMessage(pattern = '/start' , func = lambda event : Check.Access(event.message.chat_id))) 
async def Start(event) : 
    if Check.Language(event.message.chat_id) == 'en' :
        Messages = StartEn()

    elif Check.Language(event.message.chat_id) == 'fa' :
        Messages = StartFa()
    
    # WHEN THE USER ISN'T ADDED
    else : 
        Messages = StartEn()

    if not User.Exists(event.message.chat_id) :
        User.Add(event.message.chat_id) 
        await event.respond(Messages['LanguageSet'] ,\
                buttons = ButtonMaker.Inline(['English 🇬🇧' ,'فارسی 🇮🇷'] ))

    if Check.Admin(event.message.chat_id) : 
        await AdminPanel(event , Messages['HeyAdmin'])  

    # Check if user is join our channel or not  
    elif Check.IsMember(Client , event.message.chat_id) : 
            
        # If telegram account is acctive 
        if Check.Active(event.message.chat_id) : 
            await event.respond(Messages['Hi'])
                
        else : 
            await event.respond(Messages['Activate']) 
    
    else : 
        Names , Links = zip(*(map(lambda Data : [Data['Name'] , Data['Link']] , Sponsors.Data()['Channels'])))
        UrlButtons = ButtonMaker.Url(Names , Links ,  '✅')
        await event.respond(Messages['JoinChannel'], buttons = UrlButtons)

@Client.on(events.NewMessage(pattern = '/activate' , func = lambda event : Check.Access(event.message.chat_id)))
async def Activate(event) :  
    if Check.Language(event.message.chat_id)  == 'en': 
        Messages = ActivateEn()

    elif Check.Language(event.message.chat_id)  == 'fa' : 
        Messages = ActivateFa()

    # Check if user is join our channel or not  
    if Check.IsMember(Client , event.message.chat_id) :

        if Check.Active(event.message.chat_id) : 
            await event.respond(Messages['Activated'])
                
        else :
            InstaLink = 'https://www.instagram.com/' + os.getenv('InstaUsername')
            AuthKey = AuthKeyCreator(event.message.chat_id)
            await event.respond(Messages['AuthKey']+f'({InstaLink})\n`{AuthKey}`')
    
    else : 
        Names , Links = zip(*(map(lambda Data : [Data['Name'] , Data['Link']] , Sponsors.Data()['Channels'])))
        UrlButtons = ButtonMaker.Url(Names , Links ,  '✅')
        await event.respond(Messages['JoinChannel'] , buttons = UrlButtons)

@Client.on(events.NewMessage(pattern = '/feedback' , func = lambda event : Check.Access(event.message.chat_id)))
async def Feedback(event) : 
    if Check.Language == 'en' : 
        Messages = FeedbackEn(event.message.chat_id)
    
    elif Check.Language == 'fa' : 
        Messages = FeedbackFa(event.message.chat_id)

    Message = await GetReply(Messages['Feedback'] , event.message.chat_id) 
    AdminsId = Find.Admins()
    ButtonMarkup = ButtonMaker.Inline([str(event.message.chat_id)] , Data = b'TelUserId')
    for AdminId in AdminsId : 
        await Client.send_message(AdminId , '**From User : **\n    ' + Message , buttons = ButtonMarkup)

    await event.respond('Done')

@Client.on(events.NewMessage(pattern = '/help' , func = lambda event : Check.Access(event.message.chat_id)))
async def Help(event) :
    if Check.Language(event.message.chat_id) == 'en' : 
        Message = HelpEn()
    elif Check.Language(event.message.chat_id) == 'fa' : 
        Message = HelpFa()

    await event.respond(Message)


@Client.on(events.NewMessage(pattern = '/settings' , func = lambda event : Check.Access(event.message.chat_id)))
async def Settings(event) : 
    if Check.Language(event.message.chat_id) == 'en' : 
        Messages = SettingsEn()

    elif Check.Language(event.message.chat_id) == 'fa' : 
        Messages = SettingsFa()
    
    LanguageButton = ButtonMaker.Inline([Messages['BotLanguage']] , Data = b'BotLanguage')
    GroupButton = ButtonMaker.Inline([Messages['CurrentGroups']] , Data = b'Group') 
    await event.respond(Messages['Welcome'] , buttons = GroupButton + LanguageButton)


@Client.on(events.NewMessage(pattern = '/add' , func = lambda event : Check.Access(event.message.chat_id)))
async def AddGroup(event) : 
    if Check.Language(event.message.chat_id) == 'en' : 
        Messages = AddGroupEn()

    elif Check.Language(event.message.chat_id) == 'fa' : 
        Messages = AddGroupFa()
    
    GroupUsername = await GetReply(Messages['GroupUsername'] , event.message.chat_id)

    if Check.BotMembership(Client , GroupUsername) : 
        GroupChatId = Find.GroupId(Client , GroupUsername) 
        if GroupChatId : 
            Alter.Group(event.message.chat_id , GroupChatId)
            await event.respond(Messages['GroupAdded'])
            await Client.send_message(GroupChatId  , Messages['Welcome'] )

        else : 
            await event.respond(Messages['MembershipWarning'])

    else : 
        await event.respond(Messages['MembershipWarning'])

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
    TextSelection = InlineMessage.buttons[0][0].text

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
        Message = await GetReply(f'Send your message to {TextSelection}' , event.query.user_id)
        await Client.send_message(int(TextSelection) , f'**Your answer from developer : **\n    ' + Message )

    elif DataSelection == 'English 🇬🇧' : 
        Alter.Language(event.query.user_id , 'en')
        await event.edit('Successfully Completed 🫡')

    elif DataSelection == 'فارسی 🇮🇷' : 
        Alter.Language(event.query.user_id , 'fa')
        await event.edit('Successfully Completed 🫡')

    
    elif DataSelection == 'BotLanguage' :
        if Check.Language(event.query.user_id) == 'en' : 
            Messages = StartEn()

        elif Check.Language(event.query.user_id) == 'fa' : 
            Messages = StartFa()
            
        await event.edit(Messages['LanguageSet'] ,\
                buttons = ButtonMaker.Inline(['English 🇬🇧' ,'فارسی 🇮🇷'] ))
    
    elif DataSelection == 'Group' : 
        GroupId = Find.Groups(event.query.user_id)
        GroupTitle = Title if (Title := await Find.GroupTitle(Client , GroupId)) else str(GroupId) + ' : **Bot Disconnected ❌**'
        GroupJoinLink = 'https://t.me/' + await Find.GroupLink(Client , GroupId)
        await event.edit(f'[{GroupTitle}]({GroupJoinLink})')

    # Change it later
    else : 
        await event.edit('❌❌❌ There is Bug if you see it please dm me ❌❌❌')
         




def RunBot() :
    Client.start(bot_token = os.getenv('Token'))
    print('Successfully Connected !')
    Client.run_until_disconnected()
    
