from aiogram import Bot, types, Dispatcher, F
from aiogram.filters import StateFilter, Command, CommandObject, CommandStart
from aiogram.types import FSInputFile
# from aiogram.fsm.storage.memory import MemoryStorage
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

async def load_file(message: types.Message, id):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    name = os.path.basename(file_path)
    await bot.download_file(file_path, picdir+name)
    tb.del_image(id)
    tb.set_image(id, name)

async def load_photo(message: types.Message, id):
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    name = os.path.basename(file_path)
    await bot.download(file=file_id, destination=picdir+name)
    tb.del_image(id)
    tb.set_image(id, name)

async def load_video(message: types.Message, id):
    file_id = message.video.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    name =  os.path.basename(file_path)
    await bot.download_file(file_path, picdir+name)
    tb.del_image(id)
    tb.set_image(id, name)
