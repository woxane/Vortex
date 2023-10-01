def CreateEnv(Path) : 
    InstaUsername = input('Enter your Instagram Username : ')
    InstaPass = input('Enter your Instagram Password : ')
    ApiId = int(input('Enter your Telegram Bot Api Id : '))
    ApiHash = input('Enter you Telegram Bot Api Hash : ' )
    Token = input('Enter you Telegram Bot Token : ')
    # Writing config file 
    with open('../.env' , 'w') as File : 
        File.write(f'InstaUsername={InstaUsername}')
        File.write(f'\nInstaPass={InstaPass}')
        File.write(f'\nApiId={ApiId}')
        File.write(f'\nApiHash={ApiHash}')
        File.write(f'\nToken={Token}')

def CreateJson(Path , Data) :
    with open(Path , 'w') as File : 
        json.dump(Data , File , indent = 4)  
