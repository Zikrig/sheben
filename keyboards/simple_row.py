from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

def make_dobler_from_list(a:list):
    res = []
    add = []
    for f in range(len(a)):
        if f % 2 == 0:
            add = [a[f]]
        else:
            add.append(a[f])
            res.append(add)
            add = []
    if(len(a) % 2 == 1):
        res.append(add)
    # print(res)
    return res

def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    if len(items) == 0:
        return ReplyKeyboardRemove()
    row = make_dobler_from_list([KeyboardButton(text=item) for item in items])
    return ReplyKeyboardMarkup(keyboard=row, resize_keyboard=True)

def make_row_keyboard_simple(items: list[str]) -> ReplyKeyboardMarkup:
    if len(items) == 0:
        return ReplyKeyboardRemove()
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

def keyboard_proto(items: list[str]) -> ReplyKeyboardMarkup:
    if(len(items) <=2):
        row = [KeyboardButton(text=item) for item in items]
        return ReplyKeyboardMarkup(keyboard=row, resize_keyboard=True)
    
    rows = []
    for ii in range(len(items)//2 + 1):
        rows.append([KeyboardButton(text=item) for item in items[ii*2:ii*2+2]])
    return ReplyKeyboardMarkup(keyboard=rows, resize_keyboard=True)

