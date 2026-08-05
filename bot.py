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


TOKEN = "8932008249:AAH8qwRLOYUtsbO_mFJ31MMUnJbjoLWsIr4"

ADMIN_ID = 8635403087

CARD_NUMBER = "6104-3373-0010-1910"



configs = {
    "10 گیگ": {
        "price": "150 تومان",
        "time": "1 ماه"
    },

    "15 گیگ": {
        "price": "225 تومان",
        "time": "1 ماه"
    },

    "20 گیگ": {
        "price": "300 تومان",
        "time": "1 ماه"
    },

    "30 گیگ": {
        "price": "375 تومان",
        "time": "1 ماه"
    },

    "40 گیگ": {
        "price": "465 تومان",
        "time": "2 ماه"
    },

    "50 گیگ": {
        "price": "555 تومان",
        "time": "2 ماه"
    },

    "100 گیگ": {
        "price": "700 تومان",
        "time": "4 ماه"
    }
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
    ["📢 پیام همگانی"],
    ["🔙 خروج از پنل"]
]



waiting_receipt = {}

orders = {}
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



    # خرید کانفینگ

    if text == "🛒 خرید کانفینگ":


        buttons = [
            [name] for name in configs.keys()
        ]

        buttons.append(
            ["🔙 برگشت"]
        )


        await update.message.reply_text(
            "حجم کانفینگ را انتخاب کنید:",
            reply_markup=ReplyKeyboardMarkup(
                buttons,
                resize_keyboard=True
            )
        )



    # نمایش قیمت و کارت

    elif text in configs:


        config = configs[text]


        context.user_data["buy"] = text


        await update.message.reply_text(
            f"📦 کانفینگ انتخابی:\n{text}\n\n"
            f"⏳ زمان: {config['time']}\n"
            f"💰 قیمت: {config['price']}\n\n"
            f"💳 شماره کارت:\n{CARD_NUMBER}\n\n"
            "بعد از پرداخت عکس رسید را ارسال کنید 📸"
        )


        waiting_receipt[user_id] = True



    # دریافت عکس رسید

    elif text == "🔙 برگشت":


        await update.message.reply_text(
            "منوی اصلی 👇",
            reply_markup=ReplyKeyboardMarkup(
                user_menu,
                resize_keyboard=True
            )
        )
        async def photo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id


    if user_id in waiting_receipt and waiting_receipt[user_id] == True:


        photo = update.message.photo[-1]


        orders[user_id] = {
            "config": context.user_data.get("buy"),
            "status": "در انتظار تایید",
            "photo": photo.file_id
        }


        waiting_receipt[user_id] = False



        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ تایید پرداخت",
                    callback_data=f"accept_{user_id}"
                ),

                InlineKeyboardButton(
                    "❌ رد پرداخت",
                    callback_data=f"reject_{user_id}"
                )
            ]
        ]



        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo.file_id,
            caption=
            "📥 رسید جدید\n\n"
            f"👤 کاربر: {user_id}\n"
            f"📦 کانفینگ: {orders[user_id]['config']}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )



        await update.message.reply_text(
            "✅ رسید شما ارسال شد.\nمنتظر تایید باشید."
        )



    else:

        await update.message.reply_text(
            "❌ لطفاً اول خرید کانفینگ را انجام دهید."
        )




async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()


    data = query.data



    if data.startswith("accept_"):


        user_id = int(
            data.split("_")[1]
        )


        if user_id in orders:


            orders[user_id]["status"] = "تایید شده"



            await context.bot.send_message(
                chat_id=user_id,
                text=
                "✅ پرداخت شما تایید شد.\n\n"
                "کانفیگ شما به زودی ارسال می‌شود."
            )



            await query.edit_message_caption(
                "✅ پرداخت تایید شد."
            )



    elif data.startswith("reject_"):


        user_id = int(
            data.split("_")[1]
        )


        if user_id in orders:


            orders[user_id]["status"] = "رد شده"



            await context.bot.send_message(
                chat_id=user_id,
                text=
                "❌ پرداخت شما رد شد.\n"
                "لطفاً دوباره بررسی کنید."
            )


            await query.edit_message_caption(
                "❌ پرداخت رد شد."
        )
                elif text == "⭐ امتیاز من":

        await update.message.reply_text(
            "⭐ امتیاز شما: 0"
        )



    elif text == "🎁 کد هدیه":

        context.user_data["gift"] = True

        await update.message.reply_text(
            "🎁 کد هدیه خود را ارسال کنید:"
        )



    elif context.user_data.get("gift"):

        code = text

        # اینجا به دیتابیس وصل می‌شود
        # use_gift(user_id, code)

        context.user_data["gift"] = False


        await update.message.reply_text(
            "✅ کد هدیه بررسی شد."
        )



    elif text == "📊 سفارش‌ها" and user_id == ADMIN_ID:

        if orders:

            result = ""

            for uid, order in orders.items():

                result += (
                    f"👤 {uid}\n"
                    f"📦 {order['config']}\n"
                    f"📌 {order['status']}\n\n"
                )


            await update.message.reply_text(
                result
            )

        else:

            await update.message.reply_text(
                "سفارشی وجود ندارد."
            )



    elif text == "👥 کاربران" and user_id == ADMIN_ID:

        await update.message.reply_text(
            "👥 بخش کاربران"
        )



    elif text == "📢 پیام همگانی" and user_id == ADMIN_ID:

        await update.message.reply_text(
            "متن پیام را ارسال کنید."
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



print("Bot Started...")


app.run_polling()
