from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

import sqlite3


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
CREATE TABLE IF NOT EXISTS orders(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user_id INTEGER,
config TEXT,
status TEXT,
receipt TEXT
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS gifts(
code TEXT PRIMARY KEY,
points INTEGER,
used INTEGER DEFAULT 0
)
""")


db.commit()



configs = {
    "10 گیگ": "150 تومان",
    "20 گیگ": "300 تومان",
    "30 گیگ": "375 تومان",
    "50 گیگ": "555 تومان",
    "100 گیگ": "700 تومان"
}



user_menu = [
    ["🛒 خرید کانفینگ"],
    ["📦 سفارشات من"],
    ["⭐ امتیاز"],
    ["🎁 کد هدیه"]
]


admin_menu = [
    ["📊 سفارش‌ها"],
    ["🎁 ساخت هدیه"]
]


waiting_receipt = {}
selected_config = {}
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

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
            "سلام 👋\nبه ربات فروش کانفینگ خوش آمدید.",
            reply_markup=ReplyKeyboardMarkup(
                user_menu,
                resize_keyboard=True
            )
        )



async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.effective_user.id


    if text == "🛒 خرید کانفینگ":

        buttons = [
            [name] for name in configs.keys()
        ]

        buttons.append(
            ["🔙 برگشت"]
        )


        await update.message.reply_text(
            "📦 حجم کانفینگ را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                buttons,
                resize_keyboard=True
            )
        )



    elif text in configs:

        config = configs[text]

        context.user_data["buy"] = text


        await update.message.reply_text(

            f"📦 کانفینگ: {text}\n\n"
            f"⏳ زمان: {config['time']}\n"
            f"💰 قیمت: {config['price']}\n\n"
            f"💳 شماره کارت:\n{CARD_NUMBER}\n\n"
            "بعد از پرداخت عکس رسید را ارسال کنید 📸"

        )


        waiting_receipt[user_id] = True



    elif text == "📦 خریدهای من":

        await update.message.reply_text(
            "هنوز خریدی ثبت نشده است."
        )



    elif text == "⭐ امتیاز من":

        await update.message.reply_text(
            "⭐ امتیاز شما: 0"
        )



    elif text == "🎁 کد هدیه":

        await update.message.reply_text(
            "🎁 کد هدیه را ارسال کنید."
        )



    elif text == "👥 زیرمجموعه گیری":

        await update.message.reply_text(
            "لینک دعوت شما ساخته می‌شود."
        )



    elif text == "🛟 پشتیبانی":

        await update.message.reply_text(
            "پیام خود را ارسال کنید."
        )



    elif text == "🔙 برگشت":

        await update.message.reply_text(
            "منوی اصلی 👇",
            reply_markup=ReplyKeyboardMarkup(
                user_menu,
                resize_keyboard=True
            )
        )
