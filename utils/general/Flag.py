from utils.general import Config

def Check(Flag) : 
    AvilableFlags = '-E'
    if Flag not in AvilableFlags: 
        print('This Flag is not exists .')
        print('exiting ... ')
        exit()

    elif Flag == '-E' : 
        Config.EditEnv()
    
