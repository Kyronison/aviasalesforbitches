import logging
from threading import Thread
from fastapi import FastAPI
from app.routers import tickets
from app.config.database import engine
from app.models.card import Base
from apscheduler.schedulers.background import BackgroundScheduler
from app.services.ticket_service import collect_tickets  # Импорт фоновой задачи
from app.services.tickets_monitoring import run_ticket_monitoring
from app.website.application import create_app as create_website_app

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Удаление и создание таблиц (один раз при старте)
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

# Настройка планировщика
scheduler = BackgroundScheduler()
scheduler.add_job(collect_tickets, 'interval', minutes=20)
scheduler.add_job(run_ticket_monitoring, 'interval', minutes=20)
scheduler.start()

# Настройка Flask-приложения
flask_app = create_website_app()

def run_flask():
    flask_app.run(debug=False, port=5000, use_reloader=False)  # Отключаем перезагрузчик

def run_all():
    try:
        # Запуск Telegram-бота
        # bot_thread = Thread(target=run_bot)
        # bot_thread.start()
        # logger.info("Telegram-бот запущен")

        # Запуск Flask-приложения
        flask_thread = Thread(target=run_flask, daemon=True)
        flask_thread.start()
        logger.info("Flask-приложение запущено")

        # Планировщик работает в фоновом режиме
        logger.info("Все сервисы запущены. Нажмите Ctrl+C для завершения.")
        flask_thread.join()  # Поддерживаем основной поток активным
    except (KeyboardInterrupt, SystemExit):
        logger.info("Завершение работы всех сервисов")
    finally:
        scheduler.shutdown()

if __name__ == "__main__":
    logger.info("Запуск всех сервисов")
    run_all()


