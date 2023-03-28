from __init__ import types, Dispatcher, Bot, executor
from __init__ import os, myid

from regularity import *
from sql import *
import markups


bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.message):
    await bot.send_message(message.from_user.id, '''Отправь изображение с текстом чтобы начать

Для точного распознавания текста присылайте фото❗️файлом❗️иначе текст будет распознан не коректно''')
    if not db.examination(message.from_user.id):
        db.add(message.from_user.first_name, message.from_user.id, message.from_user.username)
    else:
        db.update(message.from_user.id, message.from_user.username)

@dp.message_handler(content_types=types.ContentType.ANY)
async def load_photo(message: types.Message):
    if message.chat.type == 'private':
        global id_photo
        db.update(message.from_user.id, message.from_user.username)
        if message.content_type == 'photo':
            id_photo = message.photo[-1].file_id
            await message.photo[-1].download(destination_file=f'{df.return_folderData()}\\{message.from_user.id}\\{id_photo}.jpg')
            await message.answer_photo(id_photo, reply_markup=markups.create_markupSU(id_photo))
            df.add_user_folders(str(message.from_user.id))

        if message.content_type == 'document':
            id_photo = message.document.file_id
            await message.document.download(destination_file=f'{df.return_folderData()}\\{message.from_user.id}\\{id_photo}.jpg')
            await message.answer_document(id_photo, reply_markup=markups.create_markupSU(id_photo))
            df.add_user_folders(str(message.from_user.id))

        if message.content_type == 'text':
            if message.from_user.id == myid:
                if message.text == '/clear':
                    df.clear_user_folders()
                    await message.delete()
            else:
                df.messageLoging(message.from_user.id, message.text)

@dp.callback_query_handler(text_contains="su_")
async def getText(callback: types.CallbackQuery):
    calldata = callback.data[3:]
    try:
        await bot.send_message(callback.from_user.id, convert_in_text(f"{df.return_folderData()}\\{callback.from_user.id}\\", id_photo, calldata))
        await bot.delete_message(callback.from_user.id, callback.message.message_id)
    except:
        await bot.send_message(callback.from_user.id, 'Произошла ошибка, пожалуйста повторите запрос')

executor.start_polling(dp, skip_updates=True)