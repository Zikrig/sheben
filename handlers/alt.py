from aiogram import Router
from aiogram import Bot, types, Dispatcher, F
from aiogram.filters import StateFilter, Command, CommandObject, CommandStart
from aiogram.types import FSInputFile
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from handlers.states import St
from config_base import picdir

from bot_create import tb, load_file, load_video, load_photo

from message.utils import *

router = Router()


@router.message(StateFilter(St.AltMain))
async def altpost(message: types.Message, state: FSMContext):
    to_change = message.text
    data = await state.get_data()
    post_id = str(data['post_id'])
    if to_change == '❌':
        await state.set_state(None)
        await print_message(message, post_id, True)
    elif to_change == '✏Описание':
        await state.set_state(St.AltDescribe)
        await message.answer(
            text = 'Введите новое описание для этого поста',
            reply_markup=make_row_keyboard(['❌'])
        )
    elif to_change == '✏Фото/файл':
        await state.set_state(St.AltPhoto)
        await message.answer(
            text = 'Приложите новое фото или файл для поста',
            reply_markup=make_row_keyboard(['Удалить', '❌'])
        )
    elif to_change == '✏Локация':
        await state.set_state(St.AltGeo)
        await message.answer(
            text = 'Приложите новые координаты для этого поста. \nЭто должны быть широта и долгота в десятичном формате, разделенные пробелом или на отдельных строках.\nНапример:\n53.32 61.4452',
            reply_markup=make_row_keyboard(['Удалить', '❌'])
        )

    elif to_change == 'Удалить пост':
        # await state.set_state(None)
        await message.answer(
            text = 'Пост удален'
            # reply_markup=make_row_keyboard(['Удалить', '❌'])
        )
        father = tb.get_post_by_id(post_id)['father']
        
        tb.del_post_by_id(post_id)
        
        await state.set_state(None)
        await print_message(message, father, True)

    elif to_change == 'Переименовать':
        await state.set_state(St.AltName)
        await message.answer(
            text = 'Введите новое имя для этого поста',
            reply_markup=make_row_keyboard(['❌'])
        )

@router.message(StateFilter(St.AltPhoto, St.AltDescribe, St.AltGeo, St.AltName), F.text == '❌')
async def downtomenu(message: types.Message, state: FSMContext):
    # await altpost(message, state)
    data = await state.get_data()
    post_id = str(data['post_id'])
    await print_message_to_alt_by_id(message, post_id)
    await state.set_state(St.AltMain)


@router.message(StateFilter(St.AltPhoto), F.text == 'Удалить')
async def delall(message: types.Message, state: FSMContext):
    data = await state.get_data()
    post_id = str(data['post_id'])
    tb.del_image(post_id)

    await print_message_to_alt_by_id(message, post_id)
    await state.set_state(St.AltMain)

@router.message(StateFilter(St.AltGeo), F.text == 'Удалить')
async def delall(message: types.Message, state: FSMContext):
    data = await state.get_data()
    post_id = str(data['post_id'])
    tb.del_geo(post_id)

    await print_message_to_alt_by_id(message, post_id)
    await state.set_state(St.AltMain)

@router.message(StateFilter(St.AltDescribe))
async def alt_describe(message: types.Message, state: FSMContext):
    # await altpost(message, state)
    data = await state.get_data()
    post_id = str(data['post_id'])
    new_descr = message.html_text
    if len(new_descr) > 499:
        await message.answer('Описание слишком длинное! Попробуйте уложиться в 500 знаков')
    else:
        tb.set_descr(post_id, new_descr.replace('\'', '"'))
        await message.answer('Успешно поменяли описание')
        
        await print_message_to_alt_by_id(message, post_id)
        await state.set_state(St.AltMain)

@router.message(StateFilter(St.AltName))
async def alt_name(message: types.Message, state: FSMContext):
    # await altpost(message, state)
    data = await state.get_data()
    post_id = str(data['post_id'])
    new_descr = message.text
    if len(new_descr) > 50:
        await message.answer('Имя слишком длинное! Оно не может быть больше 50 знаков')
    else:
        tb.set_name(post_id, new_descr.replace('\'', '"'))
        await message.answer('Успешно поменяли имя')
        
        await print_message_to_alt_by_id(message, post_id)
        await state.set_state(St.AltMain)

@router.message(StateFilter(St.AltPhoto))
async def alt_photo(message: types.Message, state: FSMContext):
    data = await state.get_data()
    post_id = str(data['post_id'])
    # print(message)
    
    if(message.document != '' and message.document != None):
        await load_file(message, post_id)
        await message.answer(
            text = f'Документ успешно изменен',
        )

        await print_message_to_alt_by_id(message, post_id)
        await state.set_state(St.AltMain)
    elif(message.video != '' and message.video != None):
        await load_video(message, post_id)

        await print_message_to_alt_by_id(message, post_id)
        await state.set_state(St.AltMain)
        await message.answer(
            text = f'Видео успешно изменено',
        )

    elif(message.photo != '' and message.photo != None):
        await load_photo(message, post_id)
        await message.answer(
            text = f'Фото успешно изменено',
        )
        await print_message_to_alt_by_id(message, post_id)
        await state.set_state(St.AltMain)
    else:
        await message.answer('Не нашли фото или документа')

@router.message(StateFilter(St.AltGeo))
async def alt_geo(message: types.Message, state: FSMContext):
    # await altpost(message, state)
    data = await state.get_data()
    post_id = str(data['post_id'])
    new_geo = tb.try_parse_coords(message.text)

    if not new_geo:
        await message.answer('Что-то не так с координатами, попробуйте еще раз.')
    else:
        tb.set_geo(post_id, ' '.join((str(ng) for ng in new_geo)))
        await message.answer('Успешно поменяли координаты')
        
        await print_message_to_alt_by_id(message, post_id)
        await state.set_state(St.AltMain)