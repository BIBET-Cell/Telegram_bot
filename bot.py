from telegram import Update, InputMediaPhoto, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime, timedelta

# Токен бота (замените на свой)
TOKEN = '7937428133:AAHlZ911n2Wk8kJla3n28cgJ1zXzhxQWZCM'

# Словарь для отслеживания активности пользователей
user_activity = {}

# Лимиты для анти-спама
SPAM_LIMIT = 10  # Максимальное количество сообщений
SPAM_TIME_WINDOW = 60  # Временное окно в секундах (1 минута)
BLOCK_TIME = 300  # Время блокировки в секундах (5 минут)

# Пути к скриншотам (замените на реальные пути к файлам)
SCREENSHOTS = [
    "screenshots/screenshot1.jpg",
    "screenshots/screenshot2.jpg",
    "screenshots/screenshot3.jpg",
    "screenshots/screenshot4.jpg",
    "screenshots/screenshot5.jpg"
]

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Проверяем, не заблокирован ли пользователь
    if is_user_blocked(user_id):
        blocked_until = user_activity[user_id]["blocked_until"]
        remaining_time = int((blocked_until - datetime.now()).total_seconds() // 60)
        await update.message.reply_text(
            f"⏳ Oops! You've sent too many messages. Please wait {remaining_time} minute(s) to continue."
        )
        return

    # Создаем клавиатуру с кнопками
    keyboard = [
        [KeyboardButton("🎥 Demo Video"), KeyboardButton("💳 Buy Access")],
        [KeyboardButton("ℹ️ Description")],
        [KeyboardButton("📢 Updates"), KeyboardButton("📸 Reviews")],
        [KeyboardButton("📞 Support")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Отправляем приветственное сообщение с кнопками
    welcome_message = (
        "*🔥 Welcome to the Ultimate Content Hub!* 🔥\n\n"
        "Unlock the most exclusive and private content you’ve ever seen.\n"
        "From hidden Telegram channels to secret cloud libraries — everything is here for you.\n\n"
        "👇 Choose your destiny below:"
    )
    await update.message.reply_text(welcome_message, parse_mode="Markdown", reply_markup=reply_markup)

    # Обновляем активность пользователя
    track_user_activity(user_id)

# Обработчик текстовых сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    # Проверяем, не заблокирован ли пользователь
    if is_user_blocked(user_id):
        blocked_until = user_activity[user_id]["blocked_until"]
        remaining_time = int((blocked_until - datetime.now()).total_seconds() // 60)
        await update.message.reply_text(
            f"⏳ Oops! You've sent too many messages. Please wait {remaining_time} minute(s) to continue."
        )
        return

    # Обновляем активность пользователя
    track_user_activity(user_id)

    if text == "🎥 Demo Video":
        demo_message = (
            "*🔑 Demo Access Key:* `QP8KdJr5!718D27KGT59Y&*U789Op` _(Click to copy)_\n\n"
            "[🔗 Download Link](https://drive.proton.me/urls/P6FEHQ3SC0#kKjT5HJFqiJD)\n\n"
            "_Note: Click the link above to download. The key can be copied by clicking on it._"
        )
        await update.message.reply_text(demo_message, parse_mode="Markdown", disable_web_page_preview=True)

    elif text == "💳 Buy Access":
        payment_details = (
            "*💳 Payment Method:* Cryptocurrency\n"
            "*💰 Amount:* 100.00 USD\n\n"
            "*📝 Payment Details:*\n\n"
            "▫️ ***USDT [TRC-20]***: `TPcHuYU8VVhTzU4SHqu1BgZTYzQB4tVZMn` _(Click to copy)_\n\n"
            "▫️ ***Toncoin (TON)***: `UQCid0apjKYoX5oFgNavx1WOsbRDbtynPG-54nKtShhMXq` _(Click to copy)_\n\n"
            "▫️ ***Bitcoin (BTC)***: `1GBWE9zYL8zijJpTSVFYUKkXr4PPPYAQKc` _(Click to copy)_\n\n"
            "▫️ ***Ethereum (ERC-20)***: `0x633f4df2f494db05525679047fc11063ec2ac297` _(Click to copy)_\n\n"
            "▫️ ***BNB [BEP-20]***: `0x633f4df2f494db05525679047fc11063ec2ac297` _(Click to copy)_\n\n"
            "▫️ ***Litecoin (LTC)***: `LeQc7731tVFWWe1SukcTX28vdxnm4mGoac` _(Click to copy)_\n\n"
            "For PayPal payment, contact me: [@vice_cityy](https://t.me/vice_cityy) _(Click to contact)_\n\n"
            "📋 *Instructions:*\n"
            "1. Copy the desired address by clicking on it.\n"
            "2. Send the exact amount to the address.\n"
            "3. Take a screenshot of the confirmed transfer.\n"
            "4. Send the screenshot to [@vice_cityy](https://t.me/vice_cityy) for verification.\n\n"
            "*💎 Why Choose Us?*\n"
            "We offer the most exclusive content with daily updates and a massive library of over 4.5 TB of videos and photos. "
            "Your satisfaction is our priority, and we ensure fast support and secure transactions. "
            "Join now and unlock a world of premium content!"
        )
        await update.message.reply_text(payment_details, parse_mode="Markdown", disable_web_page_preview=True)

    elif text == "ℹ️ Description":
        description = (
            "*🔒 Exclusive Access:*\n"
            "*More than +300 closed Telegram channels available in any category from A to Z — absolutely everything!*\n\n"
            "*📅 Daily Updates:*\n"
            "*Receive 10-15 fresh and exciting new links every single day with exclusive amateur content you won't find anywhere else.*\n\n"
            "*☁️ Cloud Library:*\n"
            "*Access over 4.5 TB of videos and photos in Mega, Yandex.Disk, and Mail.ru cloud storage — download and enjoy at your convenience.*\n\n"
            "*Demo videos are available below by clicking the button. This is only 0.01% of what you'll get!*"
        )
        await update.message.reply_text(description, parse_mode="Markdown", disable_web_page_preview=True)

    elif text == "📢 Updates":
        updates_message = (
            "*🔔 Latest Updates:*\n"
            "Stay tuned for the latest news and updates from our service!\n\n"
            "Join our official channel for more information:\n"
            "[📢 Updates Channel](https://t.me/+kdmfbAa8d6YyMTI6)\n\n"
            "_Note: All links in this message are clickable._"
        )
        await update.message.reply_text(updates_message, parse_mode="Markdown", disable_web_page_preview=False)

    elif text == "📸 Reviews":
        media_group = [InputMediaPhoto(open(screenshot, "rb")) for screenshot in SCREENSHOTS]
        await update.message.reply_media_group(media=media_group)

    elif text == "📞 Support":
        support_message = (
            "*💬 Support Information:*\n"
            "For payment-related questions or technical support, contact me:\n"
            "[@vice_cityy](https://t.me/vice_cityy) _(Click to contact)_\n\n"
            "_Note: All links in this message are clickable._"
        )
        await update.message.reply_text(support_message, parse_mode="Markdown", disable_web_page_preview=True)

    elif text == "🔙 Back":
        keyboard = [
            [KeyboardButton("🎥 Demo Video"), KeyboardButton("💳 Buy Access")],
            [KeyboardButton("ℹ️ Description")],
            [KeyboardButton("📢 Updates"), KeyboardButton("📸 Reviews")],
            [KeyboardButton("📞 Support")]
        ]
        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        welcome_message = (
            "*🔥 Welcome to the Ultimate Content Hub!* 🔥\n\n"
            "Unlock the most exclusive and private content you’ve ever seen.\n"
            "From hidden Telegram channels to secret cloud libraries — everything is here for you.\n\n"
            "👇 Choose your destiny below:"
        )
        await update.message.reply_text(welcome_message, parse_mode="Markdown", reply_markup=reply_markup)

    else:
        await update.message.reply_text("⚠️ Unknown command. Please use the buttons below.")

# Функция для отслеживания активности пользователя
def track_user_activity(user_id):
    now = datetime.now()
    if user_id not in user_activity:
        user_activity[user_id] = {"messages": [], "blocked_until": None}

    # Очищаем старые сообщения, которые выходят за пределы временного окна
    user_activity[user_id]["messages"] = [
        msg_time for msg_time in user_activity[user_id]["messages"]
        if now - msg_time < timedelta(seconds=SPAM_TIME_WINDOW)
    ]

    # Добавляем текущее сообщение
    user_activity[user_id]["messages"].append(now)

    # Проверяем, не превышен ли лимит
    if len(user_activity[user_id]["messages"]) > SPAM_LIMIT:
        user_activity[user_id]["blocked_until"] = now + timedelta(seconds=BLOCK_TIME)

# Функция для проверки, заблокирован ли пользователь
def is_user_blocked(user_id):
    if user_id not in user_activity:
        return False

    blocked_until = user_activity[user_id].get("blocked_until")
    if blocked_until and datetime.now() < blocked_until:
        return True

    return False

# Основная функция для запуска бота
def main():
    # Создаем приложение
    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    print("Бот запущен...")
    application.run_polling()

if __name__ == "__main__":
    main()