import logging
from threading import Thread
from pytz import timezone
from app.config.database import engine
from app.models.card import Base
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.ticket_service import collect_tickets  # Импорт фоновой задачи
from app.services.tickets_monitoring import run_ticket_monitoring
from app.website.application import create_app as create_website_app
from app.telegram_bot.bot import run_bot

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Удаление и создание таблиц (один раз при старте)
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

moscow_timezone = timezone('Europe/Moscow')

# Настройка планировщика
scheduler = BackgroundScheduler()
#scheduler.add_job(collect_tickets, 'interval', minutes=2)
scheduler.add_job(run_ticket_monitoring, 'interval', minutes=2, timezone=moscow_timezone)
scheduler.start()

# Настройка Flask-приложения
flask_app = create_website_app()

def run_flask():
    flask_app.run(debug=False, port=5000, use_reloader=False)  # Отключаем перезагрузчик


def run_all():
    try:

        flask_thread = Thread(target=run_flask, daemon=True)
        flask_thread.start()
        logger.info("Flask-приложение запущено")

        # Telegram-бот запускается в главном потоке
        logger.info("Запуск Telegram-бота в основном потоке")
        run_bot()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Завершение работы всех сервисов")
    finally:
        scheduler.shutdown()


if __name__ == "__main__":
    logger.info("Запуск всех сервисов")
    run_all()


