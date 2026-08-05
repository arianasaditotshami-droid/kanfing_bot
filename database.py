import sqlite3


DB_NAME = "users.db"


conn = sqlite3.connect(
    DB_NAME,
    check_same_thread=False
)

cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    points INTEGER DEFAULT 0
)
""")


conn.commit()



def add_user(user_id):

    cursor.execute(
        "INSERT OR IGNORE INTO users(user_id) VALUES(?)",
        (user_id,)
    )

    conn.commit()



def get_points(user_id):

    cursor.execute(
        "SELECT points FROM users WHERE user_id=?",
        (user_id,)
    )

    result = cursor.fetchone()

    if result:
        return result[0]

    return 0



def add_points(user_id, amount):

    add_user(user_id)

    cursor.execute(
        "UPDATE users SET points = points + ? WHERE user_id=?",
        (amount, user_id)
    )

    conn.commit()



def remove_points(user_id, amount):

    current = get_points(user_id)

    if current >= amount:

        cursor.execute(
            "UPDATE users SET points = points - ? WHERE user_id=?",
            (amount, user_id)
        )

        conn.commit()

        return True

    return False
