from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from config import *
from database import *


menu = [
    ["🛒 خرید کانفینگ"],
    ["📦 کانفینگ‌های خریداری‌شده"],
    ["💳 شارژ حساب"],
    ["🎁 وارد کردن کد هدیه"],
    ["👥 زیرمجموعه‌گیری"],
    ["🛟 پشتیبانی"]
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    add_user(user.id, user.username)

    await update.message.reply_text(
        "خوش آمدید 👋",
        reply_markup=ReplyKeyboardMarkup(menu, resize_keyboard=True)
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "🛒 خرید کانفینگ":
        await update.message.reply_text(
            "📦 پکیج‌ها:\n\n"
            "1- 10 گیگ\n"
            "2- 50 گیگ\n"
            "3- 100 گیگ"
        )

    elif text == "📦 کانفینگ‌های خریداری‌شده":
        await update.message.reply_text(
            "هنوز خریدی ثبت نشده است."
        )

    elif text == "💳 شارژ حساب":
        await update.message.reply_text(
            "برای شارژ حساب رسید پرداخت را ارسال کنید."
        )

    elif text == "🎁 وارد کردن کد هدیه":
        await update.message.reply_text(
            "کد هدیه خود را ارسال کنید."
        )

    elif text == "👥 زیرمجموعه‌گیری":
        await update.message.reply_text(
            "لینک اختصاصی شما ساخته می‌شود."
        )

    elif text == "🛟 پشتیبانی":
        await update.message.reply_text(
            "برای پشتیبانی پیام ارسال کنید."
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))


if __name__ == "__main__":
    app.run_polling()
