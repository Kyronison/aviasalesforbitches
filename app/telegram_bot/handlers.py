from app.telegram_bot.bot_instance import bot


def send_telegram_message(chat_id: int, message: str):
    try:
        bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")
