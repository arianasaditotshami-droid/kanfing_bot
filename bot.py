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
            "⭐️ لیست قیمت کانفینگ Plus ⭐️\n\n"
            "10 گیگ + 1 ماه = 150 تومان ❗️\n\n"
            "15 گیگ + 1 ماه = 225 تومان ❗️\n\n"
            "20 گیگ + 1 ماه = 300 تومان ❗️\n\n"
            "30 گیگ + 1 ماه = 375 تومان ❗️\n\n"
            "40 گیگ + 2 ماه = 465 تومان ❗️\n\n"
            "50 گیگ + 2 ماه = 555 تومان ❗️\n\n"
            "100 گیگ + 4 ماه = 700 تومان ❗️"
        )


    elif text == "💳 شارژ حساب":
        await update.message.reply_text(
            "💳 6104-3373-0010-1910:\n\n"
            f"{CARD_NUMBER}\n\n"
            "بعد از پرداخت رسید را ارسال کنید ✅"
        )


    elif text == "👥 زیرمجموعه‌گیری":
        bot_username = (await context.bot.get_me()).username

        link = f"https://t.me/{bot_username}?start={update.effective_user.id}"

        await update.message.reply_text(
            "👥 لینک رفرال شما:\n\n"
            f"{link}\n\n"
            "این لینک را برای دوستان خود بفرستید ✅"
        )


    elif text == "📦 کانفینگ‌های خریداری‌شده":
        await update.message.reply_text(
            "هنوز خریدی ثبت نشده است."
        )


    elif text == "🎁 وارد کردن کد هدیه":
        await update.message.reply_text(
            "کد هدیه خود را ارسال کنید."
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
