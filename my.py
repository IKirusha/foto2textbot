import telebot, os, datetime
from telebot import types
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

dir_name = 'folder'
if not os.path.isdir(dir_name):
    os.mkdir(dir_name)

TOKEN = ''
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
'''Привет🤚, я помогу вам распознать любой текст на фото.📷
Пожалуйста, введите /get, чтобы начать.\n
Языки, которые поддерживает перевод: русский, английский''')#, parse_mode='html

@bot.message_handler(commands=['get'])
def Getphoto(message):
    global ct, slovar

    list_file = []
    slovar = {}
    ct = -1

    if not os.path.isdir(dir_name + r'/' + str(message.chat.id)):
        os.mkdir(dir_name + r'/' + str(message.chat.id))

    bot.send_message(message.chat.id,
'''Отправьте фото. Для точного распознавания текста присылайте фото ❗️❗️БЕЗ сжатия❗️❗️.

    Инструкция:
    1. Нажмите значок, чтобы открыть вид галереи.
    2. Выберите изображения, которыми хотите поделиться.
    3. Нажмите кнопку с тремя точками.
    4. Выберите "Отправить без сжатия".

Процесс импорта текста может занять некоторое время.''')

    with open(fr'{dir_name}/info.txt', "a+", encoding='utf-8') as new_text:
        new_text.write(f'Пользователь {message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username} был тут {str(datetime.datetime.now())[:19]}\n')

    #######################      НЕ СЖАТОЕ фОТО        #############################################
    @bot.message_handler(content_types=['document'])
    def get_doc(message):
        global ct, slovar, chat_id
        chat_id = message.chat.id

        markup = types.InlineKeyboardMarkup(row_width=1)
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        with open(rf'{dir_name}/{message.chat.id}/{str(message.document.file_id)}.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)

        list_file.append(str(message.document.file_id)) # message.document.file_id
        if len(list_file) != 0:
            for i in list_file:
                ct += 1
                slovar.update({ct: i})
            markup.add(types.InlineKeyboardButton(f'📌 {i}', callback_data = str(ct)))
            bot.reply_to(message, f'Получить текст⤵️', reply_markup = markup)
        list_file.clear()

    #######################      СЖАТОЕ фОТО       #################################################
    @bot.message_handler(content_types=['photo'])
    def get_img(message):
        global ct, slovar, chat_id
        chat_id = message.chat.id

        markup = types.InlineKeyboardMarkup(row_width=1)
        file_info = bot.get_file(message.photo[2].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        bot.reply_to(message, '!!!Так как файл отправлен в сжатом виде, текст будет распознан некоректно!!!')

        with open(rf'{dir_name}/{message.chat.id}/{message.photo[2].file_id}.jpg', 'wb') as new_file:
            new_file.write(downloaded_file)

        list_file.append(message.photo[2].file_id)
        if len(list_file) != 0:
            for i in list_file:
                ct += 1
                slovar.update({ct: i})
            markup.add(types.InlineKeyboardButton(f'📌 {i}', callback_data = str(ct)))
            bot.reply_to(message, f'Получить текст⤵️', reply_markup = markup)
        list_file.clear()


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    try:
        for k in slovar.keys():
            if call.data == str(k):
                img = cv2.imread(f"{dir_name}\\{str(chat_id)}\\{slovar[k]}.jpg")
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                config = r'--oem 3 --psm 6'
                bot.send_message(call.message.chat.id, pytesseract.image_to_string(img, config=config, lang="rus+eng"))#
                bot.send_message(call.message.chat.id, 'В случае изменение текста, попробуйте откорректировать изображение. Для продолжения отправьте фото.')
    except:
        bot.send_message(message.chat.id, 'Ссылка устарела :(')

bot.polling(none_stop=True)
