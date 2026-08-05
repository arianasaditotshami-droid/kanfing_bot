from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

from database import (
    create_gift,
    use_gift,
    get_points,
    add_points
)


TOKEN = "8932008249:AAH8qwRLOYUtsbO_mFJ31MMUnJbjoLWsIr4"

ADMIN_ID = 8635403087

CARD_NUMBER = "6104-3373-0010-1910"



configs = {
    "10 گیگ": "10 گیگ + 1 ماه = 150 تومان",
    "15 گیگ": "15 گیگ + 1 ماه = 225 تومان",
    "20 گیگ": "20 گیگ + 1 ماه = 300 تومان",
    "30 گیگ": "30 گیگ + 1 ماه = 375 تومان",
    "40 گیگ": "40 گیگ + 2 ماه = 465 تومان",
    "50 گیگ": "50 گیگ + 2 ماه = 555 تومان",
    "100 گیگ": "100 گیگ + 4 ماه = 700 تومان"
}



menu = [
    ["🛒 خرید کانفینگ"],
    ["📦 کانفینگ‌های خریداری‌شده"],
    ["💳 شارژ حساب"],
    ["👥 زیرمجموعه‌گیری"],
    ["⭐ امتیازهای من"],
    ["🎁 وارد کردن کد هدیه"],
    ["🛟 پشتیبانی"]
]



admin_menu = [
    ["📊 سفارش‌ها"],
    ["👥 کاربران"],
    ["🎁 ساخت کد هدیه"],
    ["🔙 برگشت"]
]
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    if user_id == ADMIN_ID:

        await update.message.reply_text(
            "👑 پنل ادمین فعال شد",
            reply_markup=ReplyKeyboardMarkup(
                admin_menu,
                resize_keyboard=True
            )
        )

    else:

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



    # خرید کانفینگ

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
            configs[text] +
            "\n\n💳 مشترک عزیز لطفا بعد از پرداخت رسید را ارسال کرده و منتظر باشد توسط پشتیبانی تایید شود :\n"
            + CARD_NUMBER
        )



    elif text == "💳 شارژ حساب":

        await update.message.reply_text(
            "💳  بعد از پرداخت رسید را ارسال کنید و منتظر تایید پشتیبانی باشید:\n\n"
            + CARD_NUMBER
        )



    elif text == "📦 کانفینگ‌های خریداری‌شده":

        await update.message.reply_text(
            "هنوز سفارشی ثبت نشده."
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
                "منوی اصلی",
                reply_markup=ReplyKeyboardMarkup(
                    menu,
                    resize_keyboard=True
                )
)
                # پنل مدیریت

    elif text == "🎁 ساخت کد هدیه" and user_id == ADMIN_ID:

        context.user_data["create_gift"] = True

        await update.message.reply_text(
            "🎁 ساخت کد هدیه\n\n"
            "فرمت ارسال:\n"
            "نام_کد:تعداد_امتیاز\n\n"
            "مثال:\n"
            "HACK50:50"
        )


    elif context.user_data.get("create_gift") and user_id == ADMIN_ID:

        try:

            code, points = text.split(":")

            create_gift(
                code,
                int(points)
            )


            context.user_data["create_gift"] = False


            await update.message.reply_text(
                "✅ کد هدیه ساخته شد."
            )


        except:

            await update.message.reply_text(
                "❌ فرمت اشتباه است.\nمثال:\nHACK50:50"
            )



    elif text == "📊 سفارش‌ها" and user_id == ADMIN_ID:

        await update.message.reply_text(
            "📊 بخش سفارش‌ها در حال آماده‌سازی است."
        )



    elif text == "👥 کاربران" and user_id == ADMIN_ID:

        await update.message.reply_text(
            "👥 بخش کاربران در حال آماده‌سازی است."
        )
            # وارد کردن کد هدیه

    elif text == "🎁 وارد کردن کد هدیه":

        context.user_data["use_gift"] = True

        await update.message.reply_text(
            "🎁 کد هدیه را ارسال کنید:"
        )



    elif context.user_data.get("use_gift"):

        result = use_gift(
            user_id,
            text
        )


        context.user_data["use_gift"] = False


        if result:

            await update.message.reply_text(
                "🎉 کد هدیه فعال شد!\n"
                f"⭐ امتیاز شما: {get_points(user_id)}"
            )

        else:

            await update.message.reply_text(
                "❌ کد اشتباه است یا قبلاً استفاده شده."
            )



    elif text == "⭐ امتیازهای من":

        await update.message.reply_text(
            f"⭐ امتیاز شما: {get_points(user_id)}"
        )



    elif text == "🛟 پشتیبانی":

        await update.message.reply_text(
            "پیام خود را ارسال کنید."
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
