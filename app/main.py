from fastapi import FastAPI
from app.routers import tickets
from app.database import engine
from app.models import Base, Ticket
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import sessionmaker
import logging

Ticket.__table__.drop(engine)

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка планировщика
scheduler = BackgroundScheduler()

# Создание фабрики сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def scheduled_job():
    logger.info("Запуск задачи по сбору билетов")
    db = SessionLocal()
    try:
        logger.info("Задача по сбору билетов завершена успешно")
    except Exception as e:
        logger.error(f"Ошибка в задаче по сбору билетов: {e}")
    finally:
        db.close()

# Добавляем задачу, которая будет выполняться, например, каждые 6 часов
scheduler.add_job(scheduled_job, 'interval', hours=6)

def lifespan(app: FastAPI):
    # Код для выполнения при запуске приложения
    scheduler.start()
    yield
    # Код для выполнения при завершении приложения
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

# Подключение роутеров
app.include_router(tickets.router)
