from aiogram import Bot, types, Dispatcher, F
from aiogram.types import FSInputFile

from config_base import mysqldata, picdir
from keyboards.simple_row import *
from aiogram.fsm.storage.memory import MemoryStorage

from os import path

from bot_create import tb

def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False
    
async def print_message(message: types.Message, text: str, admin = False):
    if is_number(text):
        post = tb.get_post_by_id(text)
    else:
        post = tb.get_post_by_name(text)

    if not post:
        await message.answer('Не можем найти такого поста')
        return True 

    keyb = make_row_keyboard(post['keyboard']) if 'keyboard' in post else make_row_keyboard([])
    await answer_by_something(message, post, keyb, admin)
    

async def print_message_to_alt_by_id(message: types.Message, id: str):
    post = tb.get_post_by_id(id)
    if not post:
        await message.answer('Не можем найти такого поста')
        return False   
    
    # keyb = make_row_keyboard(post['keyboard']) if 'keyboard' in post else None
    if post['typeof'] =='hard':
        keyb = make_row_keyboard(['✏Описание', '✏Фото/файл', '✏Локация', 'Переименовать', 'Удалить пост', '❌'])
    else:
        keyb = make_row_keyboard(['✏Описание', 'Удалить пост', 'Переименовать', '❌'])
    
    # print(post)
    await answer_by_something(message, post, keyb)
    return True


async def answer_by_something(message: types.message, post, keyb, admin=False):
    if admin:
        text = post['textalt']
    else:
        text = post['textof']

    if 'image' in post and path.exists(picdir + post['image']):
        # print('image exists')
        # print(path.exists(post['image']))
        impath = picdir + post['image']
        if str(impath[-3:]).lower() in ['jpg', 'png', 'jpeg']:
            photo = FSInputFile(path=impath)
            # print('шлем изображение')
            await message.answer_photo(
                photo=photo,
                caption=text,
                parse_mode='html',
                reply_markup=keyb
            )
        elif str(impath[-3:]).lower() in ['mp4', 'wav']:
            photo = FSInputFile(path=impath)
            # print('шлем изображение')
            await message.answer_video(
                video=photo,
                caption=text,
                parse_mode='html',
                reply_markup=keyb
            )
        else:
            # print('шлем документ')
            await message.answer_document(
                document=FSInputFile(impath),
                caption=text,
                parse_mode='html',
                reply_markup=keyb
                )
    else:
        await message.answer(
            text=text,
            parse_mode='html',
            reply_markup=keyb
        )

    if 'geo' in post:
        await message.answer_location(
            latitude=post['geo'][0],
            longitude=post['geo'][1]
        )