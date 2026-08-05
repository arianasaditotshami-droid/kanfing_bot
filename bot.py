from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


TOKEN = "8932008249:AAH8qwRLOYUtsbO_mFJ31MMUnJbjoLWsIr4"
CARD_NUMBER = " 6104-3373-0010-1910"


menu = [
    ["🛒 خرید کانفینگ"],
    ["📦 کانفینگ‌های خریداری‌شده"],
    ["💳 شارژ حساب"],
    ["👥 زیرمجموعه‌گیری"],
    ["⭐ امتیازهای من"],
    ["🛟 پشتیبانی"]
]


configs = {
    "10 گیگ": "10 گیگ + 1 ماه = 150 تومان",
    "15 گیگ": "15 گیگ + 1 ماه = 225 تومان",
    "20 گیگ": "20 گیگ + 1 ماه = 300 تومان",
    "30 گیگ": "30 گیگ + 1 ماه = 375 تومان",
    "40 گیگ": "40 گیگ + 2 ماه = 465 تومان",
    "50 گیگ": "50 گیگ + 2 ماه = 555 تومان",
    "100 گیگ": "100 گیگ + 4 ماه = 700 تومان"
}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "خوش آمدید 👋",
        reply_markup=ReplyKeyboardMarkup(
            menu,
            resize_keyboard=True
        )
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text


    if text == "🛒 خرید کانفینگ":

        buttons = [[x] for x in configs]
        buttons.append(["🔙 برگشت"])

        await update.message.reply_text(
            "حجم را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                buttons,
                resize_keyboard=True
            )
        )


    elif text in configs:

        await update.message.reply_text(
            configs[text],
            reply_markup=ReplyKeyboardMarkup(
                [["🔙 برگشت"]],
                resize_keyboard=True
            )
        )


    elif text == "💳 شارژ حساب":

        await update.message.reply_text(
            f"💳 6104-3373-0010-1910شماره کارت:\n\n{CARD_NUMBER}",
            reply_markup=ReplyKeyboardMarkup(
                [["🔙 برگشت"]],
                resize_keyboard=True
            )
        )


    elif text == "📦 کانفینگ‌های خریداری‌شده":

        await update.message.reply_text(
            "هنوز خریدی ثبت نشده."
        )


    elif text == "👥 زیرمجموعه‌گیری":

        await update.message.reply_text(
            "بخش رفرال به زودی فعال می‌شود."
        )


    elif text == "⭐ امتیازهای من":

        await update.message.reply_text(
            "⭐ امتیاز شما: 0"
        )


    elif text == "🛟 پشتیبانی":

        await update.message.reply_text(
            "پیام خود را ارسال کنید."
        )


    elif text == "🔙 برگشت":

        await update.message.reply_text(
            "منوی اصلی 👇",
            reply_markup=ReplyKeyboardMarkup(
                menu,
                resize_keyboard=True
            )
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

app.run_polling()
