from sqlalchemy.orm import Session
from . import models, schemas

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

def get_tickets(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Ticket).offset(skip).limit(limit).all()