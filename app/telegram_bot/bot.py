# bot.py

import os
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from app.telegram_bot.bot_instance import application, bot  # Импортируем application и bot
from app.config.database import SessionLocal
from app.crud.users import add_chat_id_by_login

db = SessionLocal()


# Функция для приветствия при выполнении команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name  # Имя пользователя в Telegram

    if context.args:
        user_login = context.args[0]  # Логин из ссылки
        add_chat_id_by_login(db, user_login, chat_id)  # Сохраняем chat_id
        await update.message.reply_text(
            f"Привет, {user_name}! Вы подключены как пользователь с логином {user_login}. Ваш chat_id сохранён. Вот ссылка для возврата на главную страницу нашего прекрасного сайтика: http://127.0.0.1:5000"
        )
    else:
        await update.message.reply_text(
            "Ошибка: логин отсутствует! Убедитесь, что вы перешли по правильной ссылке."
        )


# Добавляем обработчик команды /start
application.add_handler(CommandHandler("start", start))


# Запускаем бота
def main():
    application.run_polling()


if __name__ == "__main__":
    main()
