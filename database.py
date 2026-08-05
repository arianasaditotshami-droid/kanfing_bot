import sqlite3

db = sqlite3.connect("bot.db")
cursor = db.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
username TEXT,
referrer INTEGER DEFAULT 0,
points INTEGER DEFAULT 0
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY,
user_id INTEGER,
config TEXT,
status TEXT,
receipt TEXT
)
""")


db.commit()



def add_user(user_id, username, referrer=0):

    cursor.execute(
        "INSERT OR IGNORE INTO users(id,username,referrer,points) VALUES (?,?,?,?)",
        (user_id, username, referrer, 0)
    )

    if referrer and referrer != user_id:

        cursor.execute(
            "UPDATE users SET points = points + 3 WHERE id=?",
            (referrer,)
        )

    db.commit()



def save_order(user_id, config):

    cursor.execute(
        "INSERT INTO orders(user_id,config,status,receipt) VALUES (?,?,?,?)",
        (user_id, config, "در انتظار پرداخت", "")
    )

    db.commit()



def save_receipt(user_id, receipt):

    cursor.execute(
        "UPDATE orders SET receipt=? WHERE user_id=? ORDER BY id DESC LIMIT 1",
        (receipt, user_id)
    )

    db.commit()



def get_user_orders(user_id):

    cursor.execute(
        "SELECT config,status FROM orders WHERE user_id=?",
        (user_id,)
    )

    return cursor.fetchall()



def get_points(user_id):

    cursor.execute(
        "SELECT points FROM users WHERE id=?",
        (user_id,)
    )

    result = cursor.fetchone()

    if result:
        return result[0]

    return 0
