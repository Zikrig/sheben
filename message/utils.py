from aiogram import Bot, types, Dispatcher, F
from aiogram.types import FSInputFile

from config_base import mysqldata, picdir
from keyboards.simple_row import *

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
    
    if admin:
        text = post['textalt']
    else:
        text = post['textof']

    # father = tb.get_post_by_name(post['father'])
    # keyb = make_row_keyboard(post['keyboard']) if 'keyboard' in post else make_row_keyboard(father['keyboard'])  if father and'keyboard' in father else None
    # print(post)
    keyb = make_row_keyboard(post['keyboard']) if 'keyboard' in post else None
    # keyb = make_row_keyboard(post['keyboard'])

    # print(post)
    if 'image' in post:
        # print('image exists')
        # print(path.exists(post['image']))
        impath = picdir + post['image']
        photo = FSInputFile(path=impath)
        await message.answer_photo(
            photo=photo,
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

async def print_message_to_alt_by_id(message: types.Message, id: str):
    post = tb.get_post_by_id(id)
    if not post:
        await message.answer('Не можем найти такого поста')
        return False   
    
    # keyb = make_row_keyboard(post['keyboard']) if 'keyboard' in post else None
    if post['typeof'] =='hard':
        keyb = make_row_keyboard(['✏Описание', '✏Фото', '✏Локация', '❌'])
    else:
        keyb = make_row_keyboard(['✏Описание', '❌'])
    
    # print(post)
    if 'image' in post:
        impath = picdir + post['image']
        photo = FSInputFile(path=impath)
        await message.answer_photo(
            photo=photo,
            caption=post['textof'],
            parse_mode='html',
            reply_markup=keyb
        )
    else:
        await message.answer(
            text=post['textof'],
            parse_mode='html',
            reply_markup=keyb
        )

    if 'geo' in post:
        await message.answer_location(
            latitude=post['geo'][0],
            longitude=post['geo'][1]
        )
    return True