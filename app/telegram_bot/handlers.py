import asyncio

from app.crud.users import add_chat_id_by_login
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from app.database import SessionLocal

db = SessionLocal()
from app.config import TELEGRAM_BOT_TOKEN, USER_MAP_FILE

def save_user_mapping(user_token, chat_id):
    if not os.path.exists(USER_MAP_FILE):
        with open(USER_MAP_FILE, 'w') as file:
            pass  # Создаём файл, если его нет

    with open(USER_MAP_FILE, 'r') as file:
        mappings = [line.strip().split(',') for line in file.readlines()]

    # Проверяем, есть ли уже такая связь
    if any(token == user_token for token, _ in mappings):
        return  # Пользователь уже сохранён

    # Сохраняем новую связь
    with open(USER_MAP_FILE, 'a') as file:
        file.write(f"{user_token},{chat_id}\n")
    print(f"Сохранён пользователь: {user_token} -> {chat_id}")


async def send_message(context):
    chat_id = context.job.data["chat_id"]
    await context.bot.send_message(chat_id=chat_id, text="Привет, ты лох!")


# Обработчик команды /start
async def start(update: Update, context):
    chat_id = update.effective_chat.id
    print(f"Получен chat_id: {chat_id}")

    if context.args:
        user_login = context.args[0]
        add_chat_id_by_login(db, user_login, chat_id)
        await update.message.reply_text(f"Вы подключены как пользователь с токеном: {user_login}")
    else:
        await update.message.reply_text("Ошибка: логин отсутствует!")


# Основная функция
def main():
    # Создаём приложение
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    application.run_polling()