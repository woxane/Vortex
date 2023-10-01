from os import getenv 
import dotenv 

def CreateEnv(Path) : 
    InstaUsername = input('Enter your Instagram Username : ')
    InstaPass = input('Enter your Instagram Password : ')
    ApiId = int(input('Enter your Telegram Bot Api Id : '))
    ApiHash = input('Enter you Telegram Bot Api Hash : ' )
    Token = input('Enter you Telegram Bot Token : ')
    # Writing config file 
    with open(Path , 'w') as File : 
        File.write(f'InstaUsername={InstaUsername}')
        File.write(f'\nInstaPass={InstaPass}')
        File.write(f'\nApiId={ApiId}')
        File.write(f'\nApiHash={ApiHash}')
        File.write(f'\nToken={Token}')

def EditEnv(Path) : 
    dotenv.load_dotenv()
    Data = {'InstaUsername' : getenv('InstaUsername') , 
            'InstaPass' : getenv('InstaPass') , 
            'ApiId' : getenv('ApiId') ,
            'ApiHash' : getenv('ApiHash') , 
            'Token' : getenv('Token') }

    for Name , Value in Data.items() : 
        print(Name + ' : ' + Value) 
        NewValue = input(f'Enter your new Value for {Name} (Enter for dont changing) : ')
        if NewValue : 
            dotenv.set_key(Path , Name ,NewValue )
    
    print('Done , run the main.py again . ') 
    exit()

def CreateJson(Path , Data) :
    with open(Path , 'w') as File : 
        json.dump(Data , File , indent = 4)  
