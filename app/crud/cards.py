from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app import models
from app.schemas import CardCreate, CityCode
from datetime import date


def create_card(db: Session, card_data: CardCreate) -> models.Card:
    """
    Создание карточки и привязка ее к пользователю.

    :param db: актуальная сессия
    :param card_data: валидная информация о карточке
    :return: объект карточки
    :raises Value error: если пользователя с таким логином нет
    :raises Value error: дата вылета раньше сегодняшнего дня (то есть уже прошла)
    """
    try:
        user = db.query(models.User).filter(models.User.login == card_data.user_login).one()
    except NoResultFound:
        raise ValueError("Пользователь не найден.")

    if card_data.flight_date < date.today():
        raise ValueError("Дата вылета не может быть в прошлом.")

    new_card = models.Card(
        user_id=user.user_id,
        origin=card_data.origin.code,
        destination=card_data.destination.code,
        flight_date=card_data.flight_date,
        price_threshold=card_data.price_threshold
    )
    db.add(new_card)
    db.commit()
    db.refresh(new_card)
    return new_card
