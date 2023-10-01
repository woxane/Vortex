import json
from os import getenv
from dotenv import load_dotenv

def JsonFile(Path) :
    try : 
        with open(Path , 'r') as File : 
            json.load(File)

        return True

    except : 
        return False

def Env(Path) : 
    load_dotenv()
    return all((getenv('InstaUsername') , getenv('InstaPass') \
            ,getenv('ApiId') ,getenv('ApiHash') , getenv('Token')))
