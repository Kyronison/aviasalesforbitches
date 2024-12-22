from telegram import Bot
from telegram.ext import Updater
from app.config.config import TELEGRAM_BOT_TOKEN

# Инициализация бота
bot = Bot(token=TELEGRAM_BOT_TOKEN)
updater = Updater(token=TELEGRAM_BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
