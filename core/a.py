from dotenv import load_dotenv

load_dotenv()

import sys
sys.path.append('../')

from handlers import events

events.RunBot()
