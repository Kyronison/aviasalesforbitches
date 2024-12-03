import asyncio
import os

import aiohttp
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from config import TOKEN, USER_MAP_FILE
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


# Функция для поиска chat_id по токену
def get_chat_id_by_token(user_token):
    if not os.path.exists(USER_MAP_FILE):
        return None

    with open(USER_MAP_FILE, 'r') as file:
        mappings = [line.strip().split(',') for line in file.readlines()]

    for token, chat_id in mappings:
        if token == user_token:
            return int(chat_id)  # chat_id возвращаем как число
    return None


# Функция для отправки сообщения в определённый chat_id
async def send_message(context):
    chat_id = context.job.data["chat_id"]
    await context.bot.send_message(chat_id=chat_id, text="Привет, ты лох!")


# Функция для отправки "Привет" всем пользователям каждые 60 секунд
async def send_hello_to_all(context):
    if not os.path.exists(USER_MAP_FILE):
        return

    with open(USER_MAP_FILE, 'r') as file:
        mappings = [line.strip().split(',') for line in file.readlines()]

    for token, chat_id in mappings:
        await context.bot.send_message(chat_id=int(chat_id), text="Привет")


async def listen_for_server_messages(application: Application):
    async with aiohttp.ClientSession() as session:
        while True:
            print(1)
            await send_hello_to_all(application.bot)
            await asyncio.sleep(5)


# Обработчик команды /start
async def start(update: Update, context):
    chat_id = update.effective_chat.id
    print(f"Получен chat_id: {chat_id}")

    if context.args:
        user_token = context.args[0]
        save_user_mapping(user_token, chat_id)
        await update.message.reply_text(f"Вы подключены как пользователь с токеном: {user_token}")
    else:
        await update.message.reply_text("Ошибка: токен отсутствует!")


# Основная функция
def main():
    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    application.run_polling()

    asyncio.create_task(listen_for_server_messages(application))