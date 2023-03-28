from __init__ import datetime, os, shutil
from __init__ import pytesseract, cv2

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class Data_files():
    def __init__(self, folder_data, message_log, bot_logs, dbName):
        self.folderDataName = folder_data
        self.messageLog = folder_data + r'/' + message_log
        self.botLogs = folder_data + r'/' + bot_logs
        self.DBNAME = folder_data + r'/' + dbName

        if not os.path.isdir(self.folderDataName):
            os.mkdir(self.folderDataName)

        if not self.messageLog in os.listdir():
            text_LOG = open(self.messageLog, "a+", encoding='utf-8')
            text_LOG.close()

        if not self.botLogs in os.listdir():
            text_LOG = open(self.botLogs, "a+", encoding='utf-8')
        text_LOG.write(f'[{str(datetime.now())[:19]}] bot is running\n')
        text_LOG.close()
        return

    def db_name(self):
        return self.DBNAME

    def return_folderData(self):
        return self.folderDataName

    def messageLoging(self, userId, message):
        with open(self.messageLog, "a+", encoding='utf-8') as mesLOG:
            mesLOG.write(f'[{str(datetime.now())[:19]}] {userId} write message: {message}\n')

    def add_user_folders(self, us_folder):
        if not os.path.isdir(self.folderDataName + r'/' + us_folder):
            os.mkdir(self.folderDataName + r'/' + us_folder)

    def clear_user_folders(self):
        for dir in os.listdir(self.folderDataName):
            dirr = self.folderDataName + '\\' + dir
            try:
                shutil.rmtree(dirr)
            except:
                ...

df = Data_files('data', 'log_chat.txt', 'logs.txt', 'dataBase.db')

def convert_in_text(patch_photo, file_name, languagy):
    img = cv2.imread(f"{patch_photo}{file_name}.jpg")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    config = r'--oem 3 --psm 6'
    _text = pytesseract.image_to_string(img, config=config, lang=languagy)
    return _text