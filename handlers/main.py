from aiogram import Router
from aiogram import Bot, types, Dispatcher, F
from aiogram.filters import StateFilter, Command, CommandObject, CommandStart
from aiogram.types import FSInputFile
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from handlers.states import St

from bot_create import tb
from config_base import admins

from message.utils import *
from aiogram.types import ContentType

router = Router()

@router.message(F.text == '/start')
async def process_start(message: types.Message):
    id = str(message.from_user.id)
    await print_message(message, '❌', id in admins)

@router.message(F.text == None)
@router.message(F.text.not_contains('/'), StateFilter(None))
async def showpost(message: types.Message):
    if message.voice:
        await imrobot(message)
        return True
    
    if not message.text in tb.posts:
        await imrobot(message)
        return True
    
    id = str(message.from_user.id)
    await print_message(message, message.text, id in admins)


@router.message(F.text.startswith('/alt_'), StateFilter(None))
async def go_to_alt(message: types.Message, state: FSMContext):
    id_adm = str(message.from_user.id)
    if not id_adm in admins:
        return False
    id = message.text.replace('/alt_', '')
    exist_post = await print_message_to_alt_by_id(message, id)
    if exist_post:
        await state.set_state(St.AltMain)
        await state.update_data(post_id=id)

# @router.message(F.text.not_contains(tb.posts.keys()))
# async def nothere(message: types.Message):
#     # id = str(message.from_user.id)
#     if message.text in tb.posts.keys():
#         await message.answer('Так вот же он')
#     else:
#         await message.answer(f'Нет ключа {message.text} в posts, только ' + ', '.join(tb.posts.keys()))