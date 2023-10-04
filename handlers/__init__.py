
def StartEn() :
    Messages = {'LanguageSet' : 'Please select the language you want to set 🗣',
    'HeyAdmin' : 'Hey Admin 🤵' , 
    'Hi' : "Hi",
    'Activate' : 'Your account is not active .\nplease activate your account with /activate .',
    'JoinChannel' : 'You must join to above channels before using the bot 🚷. \nClick ✅ after join the channel . '}
    return Messages

def StartFa() : 
    Messages = {'LanguageSet' : '🗣 لطفا زبان مد نظر خود را برای ادامه انتخاب کنید ',
    'HeyAdmin' : '🤵 سلام ادمین' , 
    'Hi' : "سلام",
    'Activate' : 'اکانت شما اکتیو نیستش . \n لطفا برای اکتیو کردن از /active استفاده کنید . ',
    'JoinChannel' : '🚷 شما قبل از استفاده از ربات باید در چنل های زیر جوین باشید . \n کلیک کنید .  ✅ بعد از جوین شدن بر روی  '}
    return Messages

def ActivateEn() : 
    Messages ={
        'Activated' : 'You are already Activated ! ' ,
        'AuthKey' : 'Send this AuthKey to [this page]' ,
        'JoinChannel' : 'You must join to above channels before using the bot 🚷. \nClick ✅ after join the channel . ' , 
    }
    return Messages

def ActivateFa() : 
    Messages ={
        'Activated' : 'اکانت شما اکتیو است . ' ,
        'AuthKey' : 'این AuthKey  را  بفرستید[به این پیج]' ,
        'JoinChannel' : '🚷 شما قبل از استفاده از ربات باید در چنل های زیر جوین باشید . \n کلیک کنید .  ✅ بعد از جوین شدن بر روی  ' , 
    }
    return Messages

def FeedbackEn() : 
    Messages = {
        'Feedback' : 'Send your feedback'
    }
    return Messages

def FeedbackFa() :
    Messages = {
        'Feedback' : 'نظرتون رو ارسال کنید '
    }
    return Messages

def HelpEn() : 
    return '''/start Welcome message
/activate Activate your account
/feedback Send a feedback to developer
/add Add a group for sending Instagram Medias separately
/help Shows the help message'''

def HelpFa(): 
    return '''/start پیام خوش آمد گویی
/activate اکتیو کردن اکانت
/feedback ارسال نظر به ادمین 
/add اضافه کردن گروه برای فرستادن جداگانه ویدیو های اینستاگرام
/help نمایش این پیغام'''

def SettingsEn() : 
    Messages = {'Welcome' :  'Welcome to the settings menu 🛠\nPlease select an option :' ,
               'BotLanguage' : 'Bot Language 🗣' }
    
    return Messages

def SettingsFa() : 
    Messages = {'Welcome' :  'به منوی تنظیمات خوش آمدید 🛠\nلطفا یک گزینه را انتخاب کنید :' ,
                'BotLanguage' : 'زبان ربات 🗣' }

    return Messages

def AddGroupEn() : 
    Messages = {
            'GroupUsername' : 'Please send the group username you want to add 💬 **with out the @**\nNote that you must add the bot to your chat 📝' , 
            'MembershipWarning' : "❌ ُThe bot isn't a member of the group you provided ❌" , 
            'GroupAdded' : 'Group username successfully added 🫡' ,
            'Welcome' : 'Hey guys 🫠' ,
            }
    
    return Messages

def AddGroupFa()  :
    Messages = {
            'GroupUsername' : 'لطاف یوزرنیم گروهی که میخواهید اضافه کنید را بفرستید 💬 **بدون @** \n اینو در نظر داشته باشید که باید بات رو به گروهتون اضافه کرده باشید 📝'  ,
            'MembershipWarning' : '❌ ُبات در حال حاضر در گروهی که دادید عضو نیست ❌' , 
            'GroupAdded' : 'یوزر نیم گروه با موفقیت اضافه شد 🫡' ,
            'Welcome' : 'سلام بچه ها 🫠' ,
            }
    
    return Messages
