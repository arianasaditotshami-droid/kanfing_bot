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



# دیتابیس

db = sqlite3.connect("bot.db", check_same_thread=False)
cursor = db.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
username TEXT,
points INTEGER DEFAULT 0
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS gifts(
code TEXT PRIMARY KEY,
points INTEGER,
used INTEGER DEFAULT 0
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
    "10 گیگ": ("150 تومان", "1 ماه"),
    "15 گیگ": ("225 تومان", "1 ماه"),
    "20 گیگ": ("300 تومان", "1 ماه"),
    "30 گیگ": ("375 تومان", "1 ماه"),
    "40 گیگ": ("465 تومان", "2 ماه"),
    "50 گیگ": ("555 تومان", "2 ماه"),
    "100 گیگ": ("700 تومان", "4 ماه")
}



user_menu = [
    ["🛒 خرید کانفینگ"],
    ["📦 خریدهای من"],
    ["⭐ امتیاز من"],
    ["🎁 کد هدیه"],
    ["👥 زیرمجموعه گیری"],
    ["🛟 پشتیبانی"]
]


admin_menu = [
    ["📊 سفارش‌ها"],
    ["👥 کاربران"],
    ["🎁 ساخت کد هدیه"],
    ["📢 پیام همگانی"]
]


waiting_receipt = {}
waiting_gift = {}
waiting_config = {}

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

    if result:
        return result[0]

    return 0




def add_points(user_id, points):

    cursor.execute(
        "UPDATE users SET points = points + ? WHERE id=?",
        (points, user_id)
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
            "سلام 👋 خوش آمدید",
            reply_markup=ReplyKeyboardMarkup(
                user_menu,
                resize_keyboard=True
            )
        )




async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.effective_user.id



    # خرید کانفینگ

    if text == "🛒 خرید کانفینگ":


        buttons = [
            [x] for x in configs.keys()
        ]

        await update.message.reply_text(
            "📦 حجم را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                buttons,
                resize_keyboard=True
            )
        )



    elif text in configs:


        price, time = configs[text]


        waiting_config[user_id] = text


        await update.message.reply_text(
            f"📦 کانفینگ: {text}\n"
            f"⏳ مدت: {time}\n"
            f"💰 قیمت: {price}\n\n"
            f"💳 شماره کارت:\n{CARD_NUMBER}\n\n"
            "بعد از پرداخت عکس رسید را ارسال کنید 📸"
        )


        waiting_receipt[user_id] = True




    elif text == "📦 خریدهای من":


        cursor.execute(
            "SELECT config,status FROM orders WHERE user_id=?",
            (user_id,)
        )

        data = cursor.fetchall()


        if data:

            msg = ""

            for x in data:

                msg += (
                    f"📦 {x[0]}\n"
                    f"📌 وضعیت: {x[1]}\n\n"
                )


            await update.message.reply_text(msg)

        else:

            await update.message.reply_text(
                "سفارشی ندارید."
            )



    elif text == "⭐ امتیاز من":

        await update.message.reply_text(
            f"⭐ امتیاز شما: {get_points(user_id)}"
        )



    elif text == "🎁 کد هدیه":

        waiting_gift[user_id] = True

        await update.message.reply_text(
            "🎁 کد هدیه را ارسال کنید:"
)
        async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id


    if waiting_receipt.get(user_id):

        photo = update.message.photo[-1].file_id

        config = waiting_config.get(
            user_id,
            "نامشخص"
        )


        cursor.execute(
            """
            INSERT INTO orders
            (user_id,config,status,receipt)
            VALUES(?,?,?,?)
            """,
            (
                user_id,
                config,
                "در انتظار تایید",
                photo
            )
        )


        db.commit()


        waiting_receipt[user_id] = False



        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ تایید",
                    callback_data=f"ok_{user_id}"
                ),

                InlineKeyboardButton(
                    "❌ رد",
                    callback_data=f"no_{user_id}"
                )
            ]
        ]



        await context.bot.send_photo(
            ADMIN_ID,
            photo,
            caption=
            f"📥 رسید جدید\n\n"
            f"👤 کاربر: {user_id}\n"
            f"📦 کانفینگ: {config}",
            reply_markup=InlineKeyboardMarkup(
                keyboard
            )
        )


        await update.message.reply_text(
            "✅ رسید ارسال شد. منتظر تایید باشید."
        )





async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


    data = query.data


    user_id = int(
        data.split("_")[1]
    )


    if data.startswith("ok"):


        cursor.execute(
            """
            UPDATE orders
            SET status=?
            WHERE user_id=?
            ORDER BY id DESC
            LIMIT 1
            """,
            (
                "تایید شده",
                user_id
            )
        )

        db.commit()



        await context.bot.send_message(
            user_id,
            "✅ پرداخت تایید شد.\nکانفیگ شما ارسال می‌شود."
        )



        await query.edit_message_caption(
            "✅ تایید شد"
        )




    elif data.startswith("no"):


        cursor.execute(
            """
            UPDATE orders
            SET status=?
            WHERE user_id=?
            ORDER BY id DESC
            LIMIT 1
            """,
            (
                "رد شده",
                user_id
            )
        )

        db.commit()



        await context.bot.send_message(
            user_id,
            "❌ پرداخت رد شد."
        )



        await query.edit_message_caption(
            "❌ رد شد"
        )






# ساخت کد هدیه توسط ادمین

async def create_gift_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return


    code = "".join(
        random.choice(string.ascii_uppercase)
        for _ in range(8)
    )


    cursor.execute(
        "INSERT INTO gifts(code,points) VALUES(?,?)",
        (
            code,
            50
        )
    )

    db.commit()


    await update.message.reply_text(
        f"🎁 کد هدیه ساخته شد:\n\n{code}\n\n⭐ 50 امتیاز"
    )



app = Application.builder().token(TOKEN).build()


app.add_handler(
    CommandHandler(
        "start",
        start
    )
)


app.add_handler(
    MessageHandler(
        filters.TEXT & ~filters.COMMAND,
        message
    )
)


app.add_handler(
    MessageHandler(
        filters.PHOTO,
        photo_handler
    )
)


app.add_handler(
    CallbackQueryHandler(
        button_handler
    )
)



app.run_polling()
