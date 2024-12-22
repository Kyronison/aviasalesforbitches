from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from app.telegram_bot.bot_instance import updater, dispatcher, bot
from app.config.database import SessionLocal
from app.crud.users import add_chat_id_by_login

db = SessionLocal()


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user_name = update.effective_user.first_name

    if context.args:
        user_login = context.args[0]
        add_chat_id_by_login(db, user_login, chat_id)
        update.message.reply_text(f"Привет, {user_name}! Вы подключены как пользователь с логином {user_login}. Ваш chat_id сохранён. Вот ссылка для возврата на главную страницу нашего прекрасного сайтика: http://127.0.0.1:5000")
    else:
        update.message.reply_text("Ошибка: логин отсутствует! Убедитесь, что вы перешли по правильной ссылке.")

# Регистрируем обработчик команды /start
dispatcher.add_handler(CommandHandler("start", start))

def run_bot():
    updater.start_polling()
    updater.idle()
