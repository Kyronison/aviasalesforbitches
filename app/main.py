# app/main.py
import time
from fastapi import FastAPI
from app.routers import tickets
from app.database import engine
from app.models import Base
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from datetime import datetime, timedelta
from app.services.aviasales_api import AviasalesAPI
from app.database import SessionLocal
from contextlib import asynccontextmanager


# Удаление всех таблиц
Base.metadata.drop_all(bind=engine)

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Настройка планировщика
scheduler = BackgroundScheduler()

def scheduled_job():
    logger.info("Запуск задачи по сбору билетов")
    db = SessionLocal()
    try:
        aviasales_api = AviasalesAPI(db=db)
        origins = ["MOW", "LED", "NYC", "LON", "PAR"]
        destinations = ["MOW", "LED", "NYC", "LON", "PAR"]
        today = datetime.today()
        days_ahead = 7  # Уменьшили количество дней вперед

        for origin in origins:
            for destination in destinations:
                if origin == destination:
                    continue  # Пропускаем, если города совпадают
                for day_offset in range(days_ahead):
                    departure_date = (today + timedelta(days=day_offset)).strftime('%Y-%m-%d')
                    try:
                        tickets = aviasales_api.get_prices_for_dates(
                            origin=origin,
                            destination=destination,
                            departure_at=departure_date,
                            currency='rub',
                            one_way=True,
                            direct=False,
                            limit=1000,
                            page=1,
                            sorting='price',
                            unique=False
                        )
                        logger.info(f"Загружено {len(tickets)} билетов для направления {origin} -> {destination} на дату {departure_date}")
                        time.sleep(0.5)  # Задержка в полсекунды между запросами
                    except Exception as e:
                        logger.error(f"Ошибка при загрузке билетов для направления {origin} -> {destination} на дату {departure_date}: {e}")
            logger.info(f"Загрузка билетов для города {origin} завершена")
        logger.info("Задача по сбору билетов завершена успешно")
    except Exception as e:
        logger.error(f"Ошибка в задаче по сбору билетов: {e}")
    finally:
        db.close()
scheduled_job()

scheduler.add_job(scheduled_job, 'interval', hours=1)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Код для выполнения при запуске приложения
    scheduler.start()
    yield
    # Код для выполнения при завершении приложения
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message": "Welcome back to aviasalesforbitches!"}

# Подключение роутеров
app.include_router(tickets.router)