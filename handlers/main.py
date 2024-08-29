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

router = Router()

@router.message(F.text == '/start')
async def process_start(message: types.Message):
    id = str(message.from_user.id)
    await print_message(message, '❌', id in admins)


@router.message(F.text.in_(tb.posts), StateFilter(None))
async def showpost(message: types.Message):
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