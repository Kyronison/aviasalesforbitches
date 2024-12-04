from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime
from typing import Optional
from app.models import Ticket


def get_ticket_by_link(db: Session, link: str):
    return db.query(models.Ticket).filter(models.Ticket.link == link).first()


def create_ticket(db: Session, ticket: schemas.TicketCreate) -> models.Ticket:
    db_ticket = models.Ticket(
        from_city=ticket.from_city,
        to_city=ticket.to_city,
        price=ticket.price,
        flight_date=ticket.flight_date,
        link=ticket.link,
        airline=ticket.airline,
        stops=ticket.stops
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket


def get_tickets_filtered(
        db: Session,
        origin: Optional[str] = None,
        destination: Optional[str] = None,
        departure_at: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        limit: int = 100
):
    query = db.query(models.Ticket)

    if origin:
        query = query.filter(models.Ticket.from_city == origin)
    if destination:
        query = query.filter(models.Ticket.to_city == destination)
    if departure_at:
        try:
            departure_date = datetime.strptime(departure_at, '%Y-%m-%d').date()
            query = query.filter(models.Ticket.flight_date == departure_date)
        except ValueError:
            raise ValueError("Некорректный формат даты. Ожидается YYYY-MM-DD.")
    if min_price is not None:
        query = query.filter(models.Ticket.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Ticket.price <= max_price)

    tickets = query.limit(limit).all()
    return tickets


def get_tickets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Ticket).offset(skip).limit(limit).all()
