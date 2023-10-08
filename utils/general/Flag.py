from utils.general import Config
from utils import Proxy

def Check(Flags) : 
    AvilableFlags = '-E -P'
    Flag = Flags[1]
    if Flag not in AvilableFlags: 
        print('This Flag is not exists .')
        print('exiting ... ')
        exit()

    elif Flag == '-E' : 
        Config.EditEnv('../.env')
    
    elif Flag == '-P' :
        try : 
            Proxy_ = Flags[2]
            return Proxy.Check(Proxy_) 

        except Exception as Excep : 
            print("There isn't any input for proxy ")
            exit()
