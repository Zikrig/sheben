from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery

from asyncio import sleep as asleep

class St(StatesGroup):
    AltMain = State()
    AltDescribe = State()
    AltPhoto = State()
    AltGeo = State()
    AltName = State()
    NewPost = State()