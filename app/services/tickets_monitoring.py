from datetime import datetime
from sqlalchemy.orm import Session
from app.services.aviasales_api import AviasalesAPI
#from app.utils.notifications import send_telegram_message
from app.models import Card
from app.database import SessionLocal
from app.crud.tickets import get_ticket_by_link, create_ticket
import logging

from app.telegram_bot.handlers import send_telegram_message

logger = logging.getLogger(__name__)


class TicketMonitor:
    def __init__(self, db: Session):
        self.db = db
        self.api = AviasalesAPI(db=self.db)

    async def check_and_notify(self):
        logger.info("Запуск мониторинга билетов")
        cards = self.db.query(Card).all()

        for card in cards:
            try:
                tickets = self.api.get_prices_for_dates(
                    origin=card.origin,
                    destination=card.destination,
                    departure_at=card.flight_date.strftime('%Y-%m-%d'),
                    currency='rub',
                    one_way=True,
                    direct=False
                )
                for ticket in tickets:
                    # Проверка на уникальность билета
                    if not get_ticket_by_link(self.db, ticket.link):
                        if ticket.price <= card.price_threshold:
                            # Отправляем уведомление пользователю
                            message = (f"🔥 Найден билет: {ticket.from_city} → {ticket.to_city}\n"
                                       f"Цена: {ticket.price} руб.\nДата вылета: {ticket.flight_date}\n"
                                       f"Ссылка: https://www.aviasales.ru/ + {ticket.link}")
                            # send_telegram_message(card.user.chat_id, message)
                            await send_telegram_message(card.user.chat_id, message)

                            logger.info(f"Билет отправлен пользователю {card.user.chat_id}")
            except Exception as e:
                logger.error(f"Ошибка для карточки {card.card_id}: {e}")

        logger.info("Мониторинг билетов завершён")


def run_ticket_monitoring():
    db = SessionLocal()
    try:
        monitor = TicketMonitor(db)
        monitor.check_and_notify()
    finally:
        db.close()
