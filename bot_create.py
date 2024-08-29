from aiogram import Bot, types, Dispatcher, F
from aiogram.filters import StateFilter, Command, CommandObject, CommandStart
from aiogram.types import FSInputFile

import re
import os
from dotenv import load_dotenv


from table.tabler import Tabler
from config_base import mysqldata, picdir


load_dotenv()

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
tb = Tabler(mysqldata)
tb.init_table_post()
# print(tb.posts)
