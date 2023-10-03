from dotenv import load_dotenv

load_dotenv()
from sys import path 
path.append('../')

from handlers import events
events.RunBot()
