# app/services/aviasales_api.py
import requests
from typing import Dict, Any, Optional, List
from app.config.config import AVIASALES_API_KEY
from sqlalchemy.orm import Session
from .. import crud, schemas
from dateutil.parser import parse
import logging

logger = logging.getLogger(__name__)

class AviasalesAPI:
    def __init__(self, db: Session):
        self.api_key = AVIASALES_API_KEY
        self.base_url = "https://api.travelpayouts.com/aviasales/v3/"
        self.db = db

    def get_prices_for_dates(
        self,
        origin: str,
        destination: str,
        departure_at: Optional[str] = None,
        return_at: Optional[str] = None,
        currency: str = 'rub',
        one_way: bool = True,
        direct: bool = False,
        limit: int = 1000,
        page: int = 1,
        sorting: str = 'price',
        unique: bool = False
    ) -> List[schemas.Ticket]:
        url = f"{self.base_url}prices_for_dates"
        params = {
            "origin": origin,
            "destination": destination,
            "departure_at": departure_at,
            "return_at": return_at,
            "one_way": str(one_way).lower(),
            "direct": str(direct).lower(),
            "currency": currency,
            "limit": limit,
            "page": page,
            "sorting": sorting,
            "unique": str(unique).lower(),
            "token": self.api_key
        }
        # Удаляем параметры со значением None
        params = {k: v for k, v in params.items() if v is not None}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # Выбрасывает исключение для статусов 4XX/5XX
            tickets_data = response.json()

            # Теперь сохраняем данные в базу данных
            added_tickets = []

            for ticket_info in tickets_data.get('data', []):
                logger.info(f"Обработка билета: {ticket_info}")

                link = ticket_info.get('deep_link') or ticket_info.get('link')
                if not link:
                    continue  # Пропускаем билеты без ссылки

                existing_ticket = crud.get_ticket_by_link(self.db, link=link)
                if existing_ticket:
                    logger.info(f"Билет уже существует: {link}")
                    continue  # Пропускаем существующие билеты

                # Парсим дату
                try:
                    flight_date = parse(ticket_info.get('departure_at')).date()
                except (ValueError, TypeError):
                    logger.warning(f"Некорректный формат даты: {ticket_info.get('departure_at')}")
                    continue  # Пропускаем билеты с некорректной датой

                # Создаём Pydantic-модель для валидации данных
                ticket_create = schemas.TicketCreate(
                    from_city=ticket_info.get('origin'),
                    to_city=ticket_info.get('destination'),
                    price=float(ticket_info.get('price')),
                    flight_date=flight_date,
                    link=link,
                    airline=ticket_info.get('airline', None),
                    stops=int(ticket_info.get('transfers', 0))
                )

                # Создаём и сохраняем билет
                #ticket = crud.create_ticket(db=self.db, ticket=ticket_create)
                added_tickets.append(ticket_create)
                #logger.info(f"Добавлен новый билет: {ticket.from_city} → {ticket.to_city} за {ticket.price} руб.")

            return added_tickets

        except requests.exceptions.RequestException as e:
            raise Exception(f"Ошибка при запросе к Aviasales API: {e}")
        except Exception as e:
            logger.error(f"Ошибка при обработке данных билетов: {e}")
            raise