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

    user = update.effective_user

    add_user(user.id, user.username)

    await update.message.reply_text(
        "خوش آمدید 👋",
        reply_markup=ReplyKeyboardMarkup(
            menu,
            resize_keyboard=True
        )
    )


async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.effective_user.id


    if text == "🛒 خرید کانفینگ":

        buttons = [[x] for x in configs.keys()]
        buttons.append(["🔙 برگشت"])

        await update.message.reply_text(
            "📦 حجم مورد نظر را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                buttons,
                resize_keyboard=True
            )
        )


    elif text in configs:

        save_order(user_id, configs[text])

        await update.message.reply_text(
            f"✅ سفارش ثبت شد\n\n"
            f"{configs[text]}\n\n"
            "💳 6104-3373-0010-1910پرداخت کنید و رسید را ارسال کنید.",
            reply_markup=ReplyKeyboardMarkup(
                [["🔙 برگشت"]],
                resize_keyboard=True
            )
        )

    elif text == "💳 شارژ حساب":

        await update.message.reply_text(
            "💳  6104-3373-0010-191شماره کارت برای پرداخت:\n\n"
            f"{CARD_NUMBER}\n\n"
            " 6104-3373-0010-1910بعد از پرداخت رسید را ارسال کنید ✅",
            reply_markup=ReplyKeyboardMarkup(
                [["🔙 برگشت"]],
                resize_keyboard=True
            )
        )


    elif text == "📦 کانفینگ‌های خریداری‌شده":

        orders = get_user_orders(user_id)

        if not orders:
            await update.message.reply_text(
                "هنوز سفارشی ندارید.",
                reply_markup=ReplyKeyboardMarkup(
                    [["🔙 برگشت"]],
                    resize_keyboard=True
                )
            )

        else:
            msg = "📦 سفارش‌های شما:\n\n"

            for order in orders:
                msg += f"🔹 {order[0]}\nوضعیت: {order[1]}\n\n"

            await update.message.reply_text(
                msg,
                reply_markup=ReplyKeyboardMarkup(
                    [["🔙 برگشت"]],
                    resize_keyboard=True
                )
            )


    elif text == "👥 زیرمجموعه‌گیری":

        bot_username = (await context.bot.get_me()).username

        link = f"https://t.me/{bot_username}?start={user_id}"

        await update.message.reply_text(
            f"👥 لینک رفرال شما:\n\n{link}",
            reply_markup=ReplyKeyboardMarkup(
                [["🔙 برگشت"]],
                resize_keyboard=True
            )
        )


    elif text == "⭐ امتیازهای من":

        await update.message.reply_text(
            "⭐ امتیاز شما: 0",
            reply_markup=ReplyKeyboardMarkup(
                [["🔙 برگشت"]],
                resize_keyboard=True
            )
                   )

    elif text == "🎁 وارد کردن کد هدیه":

        await update.message.reply_text(
            "کد هدیه خود را ارسال کنید.",
            reply_markup=ReplyKeyboardMarkup(
                [["🔙 برگشت"]],
                resize_keyboard=True
            )
        )


    elif text == "🛟 پشتیبانی":

        await update.message.reply_text(
            "برای پشتیبانی پیام ارسال کنید.",
            reply_markup=ReplyKeyboardMarkup(
                [["🔙 برگشت"]],
                resize_keyboard=True
            )
        )


    elif text == "🔙 برگشت":

        await update.message.reply_text(
            "به منوی اصلی برگشتید 👇",
            reply_markup=ReplyKeyboardMarkup(
                menu,
                resize_keyboard=True
            )
        )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))


if __name__ == "__main__":
    app.run_polling()
