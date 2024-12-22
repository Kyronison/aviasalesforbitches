from telegram import Bot
from telegram.ext import Updater
from app.config.secrets import Secrets

# Инициализация бота
bot = Bot(token=Secrets.get_secret('TELEGRAM_BOT_TOKEN'))
updater = Updater(token=Secrets.get_secret('TELEGRAM_BOT_TOKEN'), use_context=True)
dispatcher = updater.dispatcher
