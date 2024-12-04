# services/ticket_service.py
import logging
import time
from datetime import datetime, timedelta
from app.services.aviasales_api import AviasalesAPI
from app.database import SessionLocal
logger = logging.getLogger(__name__)

def collect_tickets():
    logger.info("Запуск задачи по сбору билетов")
    db = SessionLocal()
    try:
        aviasales_api = AviasalesAPI(db=db)
        origins = ["MOW", "LED", "NYC", "LON", "PAR"]
        destinations = ["MOW", "LED", "NYC", "LON", "PAR"]
        today = datetime.today()
        days_ahead = 7

        for origin in origins:
            for destination in destinations:
                if origin == destination:
                    continue
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
                        logger.info(f"Загружено {len(tickets)} билетов для {origin} -> {destination} на {departure_date}")
                        #time.sleep(0.5)
                    except Exception as e:
                        logger.error(f"Ошибка при загрузке {origin} -> {destination} на {departure_date}: {e}")
        logger.info("Сбор билетов завершен")
    except Exception as e:
        logger.error(f"Ошибка в задаче по сбору билетов: {e}")
    finally:
        db.close()
