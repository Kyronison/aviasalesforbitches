# app/telegram_bot/bot_instance.py
from telegram import Bot
from telegram.ext import Application
from app.config.config import Secrets, TELEGRAM_BOT_TOKEN


# Инициализация бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Инициализация приложения
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()