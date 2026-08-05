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


cursor.execute("""
CREATE TABLE IF NOT EXISTS admins(
id INTEGER PRIMARY KEY
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS gifts(
code TEXT PRIMARY KEY,
points INTEGER,
uses INTEGER DEFAULT 0
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



def get_points(user_id):

    cursor.execute(
        "SELECT points FROM users WHERE id=?",
        (user_id,)
    )

    result = cursor.fetchone()

    if result:
        return result[0]

    return 0



def add_admin(user_id):

    cursor.execute(
        "INSERT OR IGNORE INTO admins(id) VALUES(?)",
        (user_id,)
    )

    db.commit()



def is_admin(user_id):

    cursor.execute(
        "SELECT id FROM admins WHERE id=?",
        (user_id,)
    )

    return cursor.fetchone() is not None



def save_order(user_id, config):

    cursor.execute(
        "INSERT INTO orders(user_id,config,status,receipt) VALUES (?,?,?,?)",
        (user_id, config, "در انتظار پرداخت", "")
    )

    db.commit()



def get_orders():

    cursor.execute(
        "SELECT * FROM orders"
    )

    return cursor.fetchall()



def create_gift(code, points):

    cursor.execute(
        "INSERT INTO gifts(code,points) VALUES(?,?)",
        (code, points)
    )

    db.commit()
