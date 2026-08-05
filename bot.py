from telegram import (
    Update,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

import sqlite3
import random
import string


TOKEN = "8932008249:AAH8qwRLOYUtsbO_mFJ31MMUnJbjoLWsIr4"

ADMIN_ID = 8635403087

CARD_NUMBER = "6104-3373-0010-1910"


db = sqlite3.connect("bot.db", check_same_thread=False)
cursor = db.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
username TEXT,
points INTEGER DEFAULT 0,
referrer INTEGER DEFAULT 0
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS gifts(
code TEXT PRIMARY KEY,
points INTEGER,
used TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
config TEXT,
status TEXT,
receipt TEXT
)
""")


db.commit()



configs = {

"10 گیگ":"150 تومان - 1 ماه",
"15 گیگ":"225 تومان - 1 ماه",
"20 گیگ":"300 تومان - 1 ماه",
"30 گیگ":"375 تومان - 1 ماه",
"40 گیگ":"465 تومان - 2 ماه",
"50 گیگ":"555 تومان - 2 ماه",
"100 گیگ":"700 تومان - 4 ماه"

}



user_menu = [

["🛒 خرید کانفینگ"],
["📦 سفارش‌های من"],
["⭐ امتیاز من"],
["🎁 کد هدیه"],
["👥 زیرمجموعه گیری"]

]



admin_menu = [

["📊 سفارش‌ها"],
["🎁 ساخت کد هدیه"],
["👥 کاربران"]

]



waiting_receipt = {}
def add_user(user_id, username):

    cursor.execute(
        "INSERT OR IGNORE INTO users(id,username) VALUES(?,?)",
        (user_id, username)
    )

    db.commit()



def get_points(user_id):

    cursor.execute(
        "SELECT points FROM users WHERE id=?",
        (user_id,)
    )

    result = cursor.fetchone()

    return result[0] if result else 0



def add_points(user_id, amount):

    cursor.execute(
        "UPDATE users SET points=points+? WHERE id=?",
        (amount,user_id)
    )

    db.commit()



def create_gift(code, points):

    cursor.execute(
        "INSERT INTO gifts VALUES(?,?,?)",
        (code,points,"")
    )

    db.commit()



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user

    add_user(
        user.id,
        user.username
    )


    if user.id == ADMIN_ID:

        await update.message.reply_text(
            "👑 پنل مدیریت",
            reply_markup=ReplyKeyboardMarkup(
                admin_menu,
                resize_keyboard=True
            )
        )

    else:

        await update.message.reply_text(
            "سلام 👋",
            reply_markup=ReplyKeyboardMarkup(
                user_menu,
                resize_keyboard=True
            )
        )




async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.effective_user.id



    if text == "🛒 خرید کانفینگ":


        await update.message.reply_text(
            "حجم را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                [[x] for x in configs.keys()],
                resize_keyboard=True
            )
        )


    elif text in configs:


        cursor.execute(
            "INSERT INTO orders(user_id,config,status,receipt) VALUES(?,?,?,?)",
            (
                user_id,
                text,
                "منتظر رسید",
                ""
            )
        )

        db.commit()


        waiting_receipt[user_id] = True


        await update.message.reply_text(
            f"📦 {text}\n"
            f"💰 {configs[text]}\n\n"
            f"💳 شماره کارت:\n{CARD_NUMBER}\n\n"
            "بعد از پرداخت عکس رسید را ارسال کنید 📸"
        )



    elif text == "⭐ امتیاز من":


        await update.message.reply_text(
            f"⭐ امتیاز شما: {get_points(user_id)}"
        )




    elif text == "🎁 کد هدیه":


        context.user_data["gift"] = True


        await update.message.reply_text(
            "کد هدیه را بفرست:"
        )




    elif context.user_data.get("gift"):


        code = text


        cursor.execute(
            "SELECT points,used FROM gifts WHERE code=?",
            (code,)
        )


        result = cursor.fetchone()


        if result and result[1] == "":


            add_points(
                user_id,
                result[0]
            )


            cursor.execute(
                "UPDATE gifts SET used=? WHERE code=?",
                (str(user_id),code)
            )

            db.commit()


            await update.message.reply_text(
                "✅ 
