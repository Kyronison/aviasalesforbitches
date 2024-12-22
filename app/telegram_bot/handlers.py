# app/telegram_bot/handlers.py

from app.telegram_bot.bot_instance import bot  # Импортируем инициализированного бота

async def send_telegram_message(chat_id: int, message: str):
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        print(f"Ошибка при отправке сообщения: {e}")