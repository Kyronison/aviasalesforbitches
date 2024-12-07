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


def delete_card(db: Session, card_id: int) -> None:
    """
    Удаление карточки по id.

    :param db: актуальная сессия
    :param card_id: id карочки (int)
    :return: None
    :raise Value error: если карточка не найдена в базе данных
    """
    card = db.query(models.Card).filter(models.Card.card_id == card_id).first()
    if not card:
        raise ValueError("Карточка не найдена.")
    db.delete(card)
    db.commit()


def get_cards_by_user_login(db: Session, user_login: str) -> list[models.Card]:
    """
    Получение всех карточек пользователя по его логину.

    :param db: актуальнная сессия
    :param user_login: уникальный логин пользователя (строка)
    :return: список карточек
    :raise Value error: если пользователь не найден
    """
    try:
        user = db.query(models.User).filter(models.User.login == user_login).one()
        return user.cards
    except NoResultFound:
        raise ValueError("Такого пользователя нет в системе")


def get_card_by_id(db: Session, card_id: int) -> models.Card:
    """
    Получение карточки по id.

    :param db: актуальнная сессия
    :param card_id: id карточки (число)
    :return: объект карточки
    :raise Value error: если карточка не найдена
    """
    card = db.query(models.Card).filter(models.Card.card_id == card_id).first()
    if not card:
        raise ValueError("Такой карточки нет в системе")
    return card

