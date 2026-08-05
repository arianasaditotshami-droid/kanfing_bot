from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
import sqlite3


TOKEN = "8932008249:AAH8qwRLOYUtsbO_mFJ31MMUnJbjoLWsIr4"

ADMIN_ID = 8635403087

CARD_NUMBER = "6104-3373-0010-1910"


db = sqlite3.connect("bot.db", check_same_thread=False)
cursor = db.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
config TEXT,
status TEXT,
receipt TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
points INTEGER DEFAULT 0
)
""")


db.commit()



configs = {
    "10 گیگ": "150 تومان - 1 ماه",
    "15 گیگ": "225 تومان - 1 ماه",
    "20 گیگ": "300 تومان - 1 ماه",
    "30 گیگ": "375 تومان - 1 ماه",
    "40 گیگ": "465 تومان - 2 ماه",
    "50 گیگ": "555 تومان - 2 ماه",
    "100 گیگ": "700 تومان - 4 ماه"
}



user_menu = [
    ["🛒 خرید کانفینگ"],
    ["📦 خریدهای من"],
    ["⭐ امتیاز من"],
    ["🛟 پشتیبانی"]
]


admin_menu = [
    ["📊 سفارش‌ها"],
    ["👥 کاربران"]
]


waiting_receipt = {}



def add_user(user_id):

    cursor.execute(
        "INSERT OR IGNORE INTO users(id) VALUES(?)",
        (user_id,)
    )

    db.commit()



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    add_user(user_id)


    if user_id == ADMIN_ID:

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

        buttons = [[x] for x in configs]

        await update.message.reply_text(
            "حجم را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                buttons,
                resize_keyboard=True
            )
        )


    elif text in configs:

        waiting_receipt[user_id] = text

        await update.message.reply_text(
            f"📦 {text}\n"
            f"💰 {configs[text]}\n\n"
            f"💳 شماره کارت:\n{CARD_NUMBER}\n\n"
            "بعد از پرداخت عکس رسید را بفرستید 📸"
        )
            elif text == "📦 خریدهای من":

        cursor.execute(
            "SELECT config,status FROM orders WHERE user_id=?",
            (user_id,)
        )

        result = cursor.fetchall()


        if result:

            msg = ""

            for item in result:

                msg += (
                    f"📦 {item[0]}\n"
                    f"📌 {item[1]}\n\n"
                )

            await update.message.reply_text(msg)

        else:

            await update.message.reply_text(
                "هنوز خریدی ثبت نشده."
            )



    elif text == "⭐ امتیاز من":

        cursor.execute(
            "SELECT points FROM users WHERE id=?",
            (user_id,)
        )

        result = cursor.fetchone()

        points = result[0] if result else 0


        await update.message.reply_text(
            f"⭐ امتیاز شما: {points}"
        )



    elif text == "🛟 پشتیبانی":

        await update.message.reply_text(
            "پیام خود را ارسال کنید."
        )





async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id


    if user_id in waiting_receipt:


        config = waiting_receipt[user_id]


        file_id = update.message.photo[-1].file_id


        cursor.execute(
            "INSERT INTO orders(user_id,config,status,receipt) VALUES(?,?,?,?)",
            (
                user_id,
                config,
                "در انتظار تایید",
                file_id
            )
        )


        db.commit()


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
            chat_id=ADMIN_ID,
            photo=file_id,
            caption=
            f"📥 رسید جدید\n\n"
            f"👤 کاربر: {user_id}\n"
            f"📦 {config}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )


        del waiting_receipt[user_id]


        await update.message.reply_text(
            "✅ رسید ارسال شد. منتظر تایید باشید."
        )



async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


    data = query.data


    user_id = int(data.split("_")[1])


    if data.startswith("ok"):


        await context.bot.send_message(
            user_id,
            "✅ پرداخت تایید شد.\nکانفیگ شما ارسال می‌شود."
        )


        await query.edit_message_caption(
            "✅ تایید شد."
        )



    elif data.startswith("no"):


        await context.bot.send_message(
            user_id,
            "❌ پرداخت رد شد."
        )


        await query.edit_message_caption(
            "❌ رد شد."
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
        photo
    )
)


app.add_handler(
    CallbackQueryHandler(
        buttons
    )
)



print("Bot Started")


app.run_polling()
