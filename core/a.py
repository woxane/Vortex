import sys 
sys.path.append('../')

from dotenv import load_dotenv
load_dotenv()
from handlers import events

events.RunBot()
