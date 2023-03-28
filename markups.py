from __init__ import InlineKeyboardMarkup, InlineKeyboardButton

#k_replenish_balance = KeyboardButton('пополнить баланс')
#kb1 = ReplyKeyboardMarkup(resize_keyboard=True).add(k_replenish_balance)

def create_markupSU(callbackDATA):
    inline_keyboardsSU = InlineKeyboardMarkup()
    inline_keyboardsSU.add(InlineKeyboardButton(text=f'russian', callback_data=f'su_rus'))
    inline_keyboardsSU.add(InlineKeyboardButton(text=f'english', callback_data=f'su_eng'))
    inline_keyboardsSU.add(InlineKeyboardButton(text=f'rus&eng', callback_data=f'su_rus+eng'))
    return inline_keyboardsSU
