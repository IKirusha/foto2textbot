from __init__ import sqlite3, datetime
from regularity import df

class Database():
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def db_create(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            user_id INTEGER NOT NULL,
            first_name TEXT,
            first_date TEXT,
            last_data TEXT
        )""")
        return

    def examination(self, user_id):
        with self.connection:
            res = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(res))

    def add(self, user_name, user_id, first_name):
        with self.connection:
            return self.connection.execute("INSERT INTO users ('user_name','user_id','first_date','first_name') VALUES (?,?,?,?)", (user_name, user_id, str(datetime.now())[:19], first_name,))

    def update(self, user_id, first_name):
        with self.connection:
            return self.connection.execute("UPDATE users SET first_name = ?, last_data = ? WHERE user_id = ?", (first_name, str(datetime.now())[:19], user_id,))

db = Database(df.db_name())
db.db_create()
