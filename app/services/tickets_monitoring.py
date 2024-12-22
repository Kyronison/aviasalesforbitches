# app/services/tickets_monitoring.py

import asyncio
import logging
from sqlalchemy.orm import Session
from app.services.aviasales_api import AviasalesAPI
from app.telegram_bot.handlers import send_telegram_message
from app.models import Card
from app.schemas import TicketCreate
from app.config.database import SessionLocal
from app.crud.tickets import get_ticket_by_flight, create_ticket

logger = logging.getLogger(__name__)


class TicketMonitor:
    def __init__(self, db: Session):
        self.db = db
        self.api = AviasalesAPI(db=self.db)

    def check_and_notify(self):
        logger.info("Запуск мониторинга билетов")
        cards = self.db.query(Card).all()

        for card in cards:
            try:
                # Получаем все билеты для данного направления и даты
                tickets = self.api.get_prices_for_dates(
                    origin=card.origin,
                    destination=card.destination,
                    departure_at=card.flight_date.strftime('%Y-%m-%d'),
                    currency='rub',
                    one_way=True,
                    direct=False,
                    limit=1000,
                    page=1,
                    sorting='price',
                    unique=False
                )

                if not tickets:
                    logger.info(f"Нет доступных билетов для {card.origin} -> {card.destination} на {card.flight_date}")
                    continue

                # Находим самый дешевый билет
                cheapest_ticket = min(tickets, key=lambda x: x.price)

                # Проверяем, существует ли уже самый дешевый билет для данного направления и даты
                existing_ticket = get_ticket_by_flight(
                    self.db,
                    from_city=cheapest_ticket.from_city,
                    to_city=cheapest_ticket.to_city,
                    flight_date=cheapest_ticket.flight_date
                )

                if not existing_ticket:
                    if cheapest_ticket.price <= card.price_threshold:
                        # Формируем сообщение для пользователя
                        message = (
                            f"🔥 Найден дешевый билет!\n"
                            f"Маршрут: {cheapest_ticket.from_city} -> {cheapest_ticket.to_city}\n"
                            f"Цена: {cheapest_ticket.price} руб.\n"
                            f"Дата вылета: {cheapest_ticket.flight_date}\n"
                            f"Ссылка: https://www.aviasales.ru{cheapest_ticket.link}"
                        )
                        # Отправляем сообщение пользователю
                        send_telegram_message(card.user.chat_id, message)
                        logger.info(f"Билет отправлен пользователю {card.user.chat_id}")

                        # Создаем запись билета в базе данных
                        ticket_data = TicketCreate(
                            from_city=cheapest_ticket.from_city,
                            to_city=cheapest_ticket.to_city,
                            price=cheapest_ticket.price,
                            flight_date=cheapest_ticket.flight_date,
                            link=cheapest_ticket.link,
                            airline=cheapest_ticket.airline,
                            stops=cheapest_ticket.stops
                        )
                        create_ticket(self.db, ticket_data)
                        logger.info(f"Добавлен новый билет: {cheapest_ticket.link}")
                    else:
                        logger.info(
                            f"Самый дешевый билет ({cheapest_ticket.price} руб.) выше порога для карточки {card.card_id}"
                        )
                else:
                    logger.info(f"Самый дешевый билет уже существует в базе: {existing_ticket.link}")

            except Exception as e:
                logger.error(f"Ошибка для карточки {card.card_id}: {e}")

        logger.info("Мониторинг билетов завершён")


def run_ticket_monitoring():
    db = SessionLocal()
    try:
        monitor = TicketMonitor(db)
        asyncio.run(monitor.check_and_notify())
    except Exception as e:
        logger.error(f"Ошибка в задаче мониторинга билетов: {e}")
    finally:
        db.close()
