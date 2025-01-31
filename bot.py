import os
import telebot
from flask import Flask, request
from datetime import datetime, timedelta

# Получаем токен бота из переменной окружения
TOKEN = os.getenv("TELEGRAM_TOKEN", "7937428133:AAHlZ911n2Wk8kJla3n28cgJ1zXzhxQWZCM")
if not TOKEN:
    raise ValueError("TELEGRAM_TOKEN не найден в переменных окружения!")

# ID администратора (ваш ID)
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "6329950188"))

# Создаем экземпляр бота
bot = telebot.TeleBot(TOKEN)

# Создаем Flask-сервер
app = Flask(__name__)

# Словарь для отслеживания активности пользователей
user_activity = {}

# Лимиты для анти-спама
SPAM_LIMIT = 10  # Максимальное количество сообщений
SPAM_TIME_WINDOW = 60  # Временное окно в секундах (1 минута)
BLOCK_TIME = 300  # Время блокировки в секундах (5 минут)

# Пути к скриншотам для кнопки "Reviews"
REVIEWS_SCREENSHOTS = [
    "screenshots/review1.jpg",
    "screenshots/review2.jpg",
    "screenshots/review3.jpg",
    "screenshots/review4.jpg",
    "screenshots/review5.jpg"
]

# Пути к скриншотам для кнопки "Proof"
PROOF_SCREENSHOTS = [
    "screenshots/proof1.jpg",
    "screenshots/proof2.jpg",
    "screenshots/proof3.jpg"
]

# Подписи для кнопки "Proof"
PROOF_CAPTIONS = [
    "Screenshot 1: Exclusive content preview.",
    "Screenshot 2: Daily updates section.",
    "Screenshot 3: Cloud library access."
]

# Базовый маршрут для проверки работы
@app.route("/", methods=["GET"])
def home():
    return "Telegram bot is running! 🚀", 200

# Маршрут для Webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    # Получаем обновление от Telegram
    update = request.get_json()
    if update:
        bot.process_new_updates([telebot.types.Update.de_json(update)])
    return "OK", 200

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    # Проверяем, не заблокирован ли пользователь
    if is_user_blocked(user_id):
        blocked_until = user_activity[user_id]["blocked_until"]
        remaining_time = int((blocked_until - datetime.now()).total_seconds() // 60)
        bot.send_message(
            message.chat.id,
            f"⏳ Oops! You've sent too many messages. Please wait {remaining_time} minute(s) to continue."
        )
        return

    # Создаем клавиатуру с кнопками
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        ["🎥 Demo Video", "💳 Buy Access"],
        ["ℹ️ Description"],
        ["📢 Updates", "📸 Reviews"],
        ["📞 Support", "📋 Proof"]
    ]
    keyboard.add(*[telebot.types.KeyboardButton(button) for row in buttons for button in row])

    # Отправляем приветственное сообщение с кнопками
    welcome_message = (
        "*🔥 Welcome to the Ultimate Content Hub!* 🔥\n\n"
        "Unlock the most exclusive and private content you’ve ever seen.\n"
        "From hidden Telegram channels to secret cloud libraries — everything is here for you.\n\n"
        "👇 Choose your destiny below:"
    )
    bot.send_message(message.chat.id, welcome_message, parse_mode="Markdown", reply_markup=keyboard)

    # Обновляем активность пользователя
    track_user_activity(user_id)

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text

    # Проверяем, не заблокирован ли пользователь
    if is_user_blocked(user_id):
        blocked_until = user_activity[user_id]["blocked_until"]
        remaining_time = int((blocked_until - datetime.now()).total_seconds() // 60)
        bot.send_message(
            message.chat.id,
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
        bot.send_message(message.chat.id, demo_message, parse_mode="Markdown", disable_web_page_preview=True)

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
        bot.send_message(message.chat.id, payment_details, parse_mode="Markdown", disable_web_page_preview=True)

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
        bot.send_message(message.chat.id, description, parse_mode="Markdown", disable_web_page_preview=True)

    elif text == "📢 Updates":
        updates_message = (
            "*🔔 Latest Updates:*\n"
            "Stay tuned for the latest news and updates from our service!\n\n"
            "Join our official channel for more information:\n"
            "[📢 Updates Channel](https://t.me/+kdmfbAa8d6YyMTI6)\n\n"
            "_Note: All links in this message are clickable._"
        )
        bot.send_message(message.chat.id, updates_message, parse_mode="Markdown", disable_web_page_preview=False)

    elif text == "📸 Reviews":  # Обработка кнопки "📸 Reviews"
        review_message = (
            "*📸 User Reviews:*\n"
            "Here are some screenshots from our satisfied users. Enjoy! 😊"
        )
        bot.send_message(message.chat.id, review_message, parse_mode="Markdown")

        media_group = []
        files = []  # Список для хранения открытых файлов

        for i in range(5):  # Отправляем 5 скриншотов
            try:
                file = open(REVIEWS_SCREENSHOTS[i], "rb")
                files.append(file)  # Добавляем файл в список
                media_group.append(telebot.types.InputMediaPhoto(file, caption=f"Review Screenshot {i + 1}"))
            except FileNotFoundError:
                bot.send_message(message.chat.id, f"❌ File not found: {REVIEWS_SCREENSHOTS[i]}")
                return

        try:
            bot.send_media_group(message.chat.id, media_group)
        finally:
            for file in files:  # Закрываем все файлы после отправки
                file.close()

    elif text == "📞 Support":
        support_message = (
            "*💬 Support Information:*\n"
            "For payment-related questions or technical support, contact me:\n"
            "[@vice_cityy](https://t.me/vice_cityy) _(Click to contact)_\n\n"
            "_Note: All links in this message are clickable._"
        )
        bot.send_message(message.chat.id, support_message, parse_mode="Markdown", disable_web_page_preview=True)

    elif text == "📋 Proof":  # Обработка кнопки "Proof"
        proof_message = (
            "*📋 Proof of Content:*\n"
            "Here are some screenshots to prove the quality of our content. Enjoy! 😊"
        )
        bot.send_message(message.chat.id, proof_message, parse_mode="Markdown")

        media_group = []
        files = []  # Список для хранения открытых файлов

        for i in range(3):  # Отправляем 3 скриншота с подписями
            try:
                file = open(PROOF_SCREENSHOTS[i], "rb")
                files.append(file)  # Добавляем файл в список
                media_group.append(telebot.types.InputMediaPhoto(file, caption=PROOF_CAPTIONS[i]))
            except FileNotFoundError:
                bot.send_message(message.chat.id, f"❌ File not found: {PRO