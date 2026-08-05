import sqlite3

db = sqlite3.connect("bot.db")
cursor = db.cursor()


# کاربران
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
username TEXT,
referrer INTEGER DEFAULT 0,
points INTEGER DEFAULT 0
)
""")


# سفارش‌ها
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY,
user_id INTEGER,
config TEXT,
status TEXT,
receipt TEXT
)
""")


# ادمین‌ها
cursor.execute("""
CREATE TABLE IF NOT EXISTS admins(
id INTEGER PRIMARY KEY
)
""")


# کدهای هدیه
cursor.execute("""
CREATE TABLE IF NOT EXISTS gifts(
id INTEGER PRIMARY KEY,
code TEXT UNIQUE,
points INTEGER,
used INTEGER DEFAULT 0
)
""")


# استفاده کاربران از هدیه
cursor.execute("""
CREATE TABLE IF NOT EXISTS used_gifts(
id INTEGER PRIMARY KEY,
user_id INTEGER,
gift_code TEXT
)
""")


db.commit()



def add_points(user_id, amount):

    cursor.execute(
        "UPDATE users SET points = points + ? WHERE id=?",
        (amount, user_id)
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



def create_gift(code, points):

    cursor.execute(
        "INSERT INTO gifts(code,points) VALUES(?,?)",
        (code, points)
    )

    db.commit()



def use_gift(user_id, code):

    cursor.execute(
        "SELECT points FROM gifts WHERE code=?",
        (code,)
    )

    gift = cursor.fetchone()

    if not gift:
        return False


    cursor.execute(
        "SELECT id FROM used_gifts WHERE user_id=? AND gift_code=?",
        (user_id, code)
    )

    used = cursor.fetchone()

    if used:
        return False


    add_points(user_id, gift[0])


    cursor.execute(
        "INSERT INTO used_gifts(user_id,gift_code) VALUES(?,?)",
        (user_id, code)
    )

    db.commit()

    return True
