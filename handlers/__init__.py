

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
/help Shows the help message'''

def HelpFa(): 
    return '''/start پیام خوش آمد گویی
/activate اکتیو کردن اکانت
/feedback ارسال نظر به ادمین 
/help نمایش این پیغام'''

def SettingsEn() : 
    return 'Welcome to the settings menu 🛠\nPlease select an option :'


def SettingsEn() : 
    return 'به منوی تنظیمات خوش آمدید 🛠\nلطفا یک گزینه را انتخاب کنید :'

