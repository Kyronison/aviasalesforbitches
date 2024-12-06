import pytest
from unittest.mock import patch
from sqlalchemy.orm.exc import NoResultFound
from app.crud import cards
from app import models
from app.schemas import CardCreate, CityCode
from datetime import date, timedelta


@pytest.fixture
def valid_card_data():
    return CardCreate(
        user_login="testuser",
        origin=CityCode(code="MOV"),
        destination=CityCode(code="LED"),
        flight_date=date.today() + timedelta(days=10),
        price_threshold=500
    )


def test_create_card_success(mock_db_session, valid_card_data):
    """Тест успешного создания карточки"""
    mock_user = models.User(login="testuser", user_id=1)
    mock_db_session.query().filter(models.User.login == "testuser").one.return_value = mock_user

    created_card = cards.create_card(mock_db_session, valid_card_data)

    assert created_card.user_id == 1
    assert created_card.origin == "MOV"
    assert created_card.destination == "LED"
    assert created_card.flight_date == valid_card_data.flight_date
    assert created_card.price_threshold == 500


def test_create_card_user_not_found(mock_db_session, valid_card_data):
    """Тест неудачного создания карточки из-за отсутствия пользователя в системе"""
    mock_db_session.query().filter(models.User.login == "nonexistentuser").one.side_effect = NoResultFound

    with pytest.raises(ValueError) as e:
        cards.create_card(mock_db_session, valid_card_data)
    assert str(e.value) == "Пользователь не найден."


def test_create_card_past_date(mock_db_session, valid_card_data):
    """Тест неудачного создания карточки из-за прошедшей даты"""
    mock_user = models.User(login="testuser", user_id=1)
    mock_db_session.query().filter(models.User.login == "testuser").one.return_value = mock_user
    past_date = date.today() - timedelta(days=1)
    invalid_card_data = valid_card_data.copy(update={"flight_date": past_date})

    with pytest.raises(ValueError) as e:
        cards.create_card(mock_db_session, invalid_card_data)
    assert str(e.value) == "Дата вылета не может быть в прошлом."


def test_delete_card_success(mock_db_session):
    """Тест успешного удаления карточки"""
    mock_card = models.Card(card_id=1)
    mock_db_session.query().filter(models.Card.card_id == 1).first.return_value = mock_card

    cards.delete_card(mock_db_session, 1)

    mock_db_session.query().filter(models.Card.card_id == 1).first.assert_called_once()
    mock_db_session.query().filter(models.Card.card_id == 1).first.return_value = None


def test_delete_card_not_found(mock_db_session):
    """Тест неудачного удаления карточки из-за того что ее нет в базе"""
    mock_db_session.query().filter(models.Card.card_id == 999).first.return_value = None

    with pytest.raises(ValueError) as e:
        cards.delete_card(mock_db_session, 999)
    assert str(e.value) == "Карточка не найдена."


def test_get_cards_by_user_login_success(mock_db_session):
    """Тест успешного получения карточек пользователя"""
    mock_user = models.User(login="testuser", cards=[models.Card(card_id=1), models.Card(card_id=2)])
    mock_db_session.query().filter(models.User.login == "testuser").one.return_value = mock_user

    retrieved_cards = cards.get_cards_by_user_login(mock_db_session, "testuser")

    assert len(retrieved_cards) == 2
    assert retrieved_cards[0].card_id == 1
    assert retrieved_cards[1].card_id == 2


def test_get_cards_by_user_login_user_not_found(mock_db_session):
    """Тест неудачного получения карточек пользователя из-зи отсутствия пользователя в базе"""
    mock_db_session.query().filter(models.User.login == "nonexistentuser").one.side_effect = NoResultFound

    with pytest.raises(ValueError) as e:
        cards.get_cards_by_user_login(mock_db_session, "nonexistentuser")
    assert str(e.value) == "Такого пользователя нет в системе"


def test_get_cards_by_user_login_no_cards(mock_db_session):
    """Тест пользователь найден, но карточек нет"""
    mock_user = models.User(login="testuser", cards=[])
    mock_db_session.query().filter(models.User.login == "testuser").one.return_value = mock_user

    retrieved_cards = cards.get_cards_by_user_login(mock_db_session, "testuser")

    assert len(retrieved_cards) == 0
