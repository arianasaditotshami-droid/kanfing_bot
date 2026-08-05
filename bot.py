from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


TOKEN = "8932008249:AAH8qwRLOYUtsbO_mFJ31MMUnJbjoLWsIr4"
CARD_NUMBER = "6104337300101910"

ADMIN_ID = 8635403087


menu = [
    ["🛒 خرید کانفینگ"],
    ["📦 کانفینگ‌های خریداری‌شده"],
    ["💳 شارژ حساب"],
    ["⭐ امتیازهای من"],
    ["🎁 کد هدیه"],
    ["🛟 پشتیبانی"]
]


admin_menu = [
    ["📊 سفارش‌ها"],
    ["👥 کاربران"],
    ["➕ افزودن امتیاز"],
    ["🎁 ساخت کد هدیه"],
    ["🔙 برگشت"]
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


# ذخیره امتیاز کاربران (فعلاً موقت)
points = {}



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id not in points:
        points[user_id] = 0


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
            "سلام 👋 خوش آمدید",
            reply_markup=ReplyKeyboardMarkup(
                menu,
                resize_keyboard=True
            )
        )



async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text
    user_id = update.effective_user.id



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

        await update.message

    elif text == "⭐ امتیازهای من":

        user_points = points.get(user_id, 0)

        await update.message.reply_text(
            "⭐ امتیازهای شما\n\n"
            f"⭐ امتیاز فعلی: {user_points}\n\n"
            "🎁 امتیازها برای دریافت هدیه استفاده می‌شوند."
        )


    elif text == "➕ افزودن امتیاز":

        if user_id == ADMIN_ID:

            await update.message.reply_text(
                "👤 آیدی کاربر و مقدار امتیاز را اینطوری بفرست:\n\n"
                "مثال:\n"
                "123456789 50"
            )

            context.user_data["add_point"] = True


    elif context.user_data.get("add_point"):

        if user_id == ADMIN_ID:

            try:

                data = text.split()

                target_id = int(data[0])
                amount = int(data[1])

                points[target_id] = points.get(target_id, 0) + amount

                await update.message.reply_text(
                    "✅ امتیاز با موفقیت اضافه شد."
                )

                context.user_data["add_point"] = False


            except:

                await update.message.reply_text(
                    "❌ فرمت اشتباه است."
                )



    elif text == "🎁 کد هدیه":

        await update.message.reply_text(
            "🎁 کد هدیه را ارسال کنید."
        )



    elif text == "🛟 پشتیبانی":

        await update.message.reply_text(
            "پیام خود را ارسال کنید."
        )



    elif text == "🔙 برگشت":

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
                "منوی اصلی 👇",
                reply_markup=ReplyKeyboardMarkup(
                    menu,
                    resize_keyboard=True
                )
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


app.run_polling()
