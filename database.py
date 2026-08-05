import sqlite3

db = sqlite3.connect("bot.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
username TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS configs(
id INTEGER PRIMARY KEY,
user_id INTEGER,
config TEXT
)
""")

db.commit()


def add_user(user_id, username):
    cursor.execute(
        "INSERT OR IGNORE INTO users VALUES (?,?)",
        (user_id, username)
    )
    db.commit()


def save_config(user_id, text):
    cursor.execute(
        "INSERT INTO configs(user_id,config) VALUES (?,?)",
        (user_id,text)
    )
    db.commit()
