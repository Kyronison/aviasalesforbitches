# test_aviasales_api.py

import sys
import os

# Добавляем путь к директории проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.aviasales_api import AviasalesAPI
from app.database import SessionLocal
from app.models import Base, Ticket
from app.database import engine
import logging


def main():
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Создание таблиц в базе данных, если они не существуют
    Base.metadata.create_all(bind=engine)

    # Создание сессии базы данных
    db_session = SessionLocal()

    try:
        # Создаем экземпляр AviasalesAPI с передачей сессии базы данных
        aviasales_api = AviasalesAPI(db=db_session)

        # Вызов метода get_prices_for_dates с нужными параметрами
        tickets = aviasales_api.get_prices_for_dates(
            origin='MOW',
            destination='LED',
            departure_at='2024-12-31',
            return_at='2025-01-01',
            currency='rub',
            one_way=False,
            direct=False,
        )

        # Проверяем, получили ли мы билеты
        if tickets:
            prices = [ticket.price for ticket in tickets if ticket.price is not None]

            if prices:
                average_price = sum(prices) / len(prices)
                min_price = min(prices)
                max_price = max(prices)

                print(f"Найдено билетов: {len(prices)}")
                print(f"Средняя цена билетов: {average_price:.2f} руб")
                print(f"Минимальная цена: {min_price} руб")
                print(f"Максимальная цена: {max_price} руб")
            else:
                print("Не удалось найти цены в полученных билетах.")
        else:
            print("Билеты не были получены или добавлены.")
    except Exception as e:
        print(f"Произошла ошибка при получении данных: {e}")
    finally:
        # Закрываем сессию базы данных
        db_session.close()


if __name__ == "__main__":
    main()