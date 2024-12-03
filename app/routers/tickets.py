# app/routers/tickets.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from .. import crud, schemas
from ..dependencies import get_db
from ..services.aviasales_api import AviasalesAPI

router = APIRouter(
    prefix="/tickets",
    tags=["tickets"]
)

@router.post("/fetch", response_model=List[schemas.Ticket])
def fetch_tickets(
    origin: str = Query(..., description="Код города отправления (например, 'MOW')"),
    destination: str = Query(..., description="Код города назначения (например, 'LED')"),
    departure_at: str = Query(..., description="Дата вылета в формате 'YYYY-MM-DD' (например, '2024-05-01')"),
    db: Session = Depends(get_db)
):
    """
    Получить билеты от Aviasales API и сохранить их в базу данных.
    """
    try:
        aviasales_api = AviasalesAPI(db=db)
        tickets = aviasales_api.get_prices_for_dates(
            origin=origin,
            destination=destination,
            departure_at=departure_at,
            currency='rub',
            one_way=False,
            direct=False,
        )
        return tickets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))