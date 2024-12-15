import asyncio
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from app.crud.users import add_chat_id_by_login
from app.database import SessionLocal
from app.telegram_bot.config import TOKEN

db = SessionLocal()
application = None
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")



# Функция для приветствия при выполнении команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name  # Имя пользователя в Telegram

    if context.args:
        user_login = context.args[0]  # Логин из ссылки
        # add_chat_id_by_login(db, user_login, chat_id)  # Сохраняем chat_id
        await update.message.reply_text(
            f"Привет, {user_name}! Вы подключены как пользователь с логином {user_login}. Ваш chat_id сохранён."
        )
    else:
        await update.message.reply_text(
            "Ошибка: логин отсутствует! Убедитесь, что вы перешли по правильной ссылке."
        )


# Функция для отправки сообщения по chat_id
async def send_telegram_message(chat_id: int, message: str):
    try:
        await application.bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")


# Запускаем бота
def main():
    global application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    application.run_polling()
