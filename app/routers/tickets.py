# app/routers/tickets.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import crud, schemas
from ..dependencies import get_db

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)

@router.get("/", response_model=List[schemas.Ticket])
def get_tickets(
    origin: str = Query(None, description="Код города отправления (например, 'MOW')"),
    destination: str = Query(None, description="Код города назначения (например, 'LED')"),
    departure_at: Optional[str] = Query(None, description="Дата вылета в формате 'YYYY-MM-DD'"),
    min_price: Optional[float] = Query(None, description="Минимальная цена"),
    max_price: Optional[float] = Query(None, description="Максимальная цена"),
    limit: int = Query(100, description="Количество записей для возврата"),
    db: Session = Depends(get_db)
):
    """
    Получить список билетов из базы данных по заданным критериям.
    """
    try:
        tickets = crud.get_tickets_filtered(
            db=db,
            origin=origin,
            destination=destination,
            departure_at=departure_at,
            min_price=min_price,
            max_price=max_price,
            limit=limit
        )
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))