import pytest
from app.crud import users
from unittest.mock import patch
from sqlalchemy.orm.exc import NoResultFound
from app import models, schemas
from tests.conftest import mock_db_session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@pytest.mark.parametrize("login, expected", [("unique_login", True), ("duplicate_login", False)])
def test_is_login_unique(mock_db_session, login, expected):
    """Тест функции на проверку уникальности логина"""
    mock_user = models.User(login=login) if expected is False else None
    mock_db_session.query().filter(models.User.login == login).first.return_value = mock_user
    result = users.__is_login_unique(mock_db_session, login)
    assert result == expected


@patch('app.crud.users.security.hash_password', return_value="mocked_hash")
def test_create_user_success(mock_hash_password, mock_db_session):
    """Тест успешного создания пользователя"""
    new_user_data = schemas.UserCreate(login="testuser", password="pswrd123")
    with patch('app.crud.users.__is_login_unique', return_value=True):
        created_user = users.create_user(mock_db_session, new_user_data)

    assert created_user.login == "testuser"
    assert created_user.hashed_password == "mocked_hash"

    mock_hash_password.assert_called_once()
    mock_hash_password.assert_called_once()  # Проверяем, что hash_password не вызывался


@patch('app.crud.users.security.hash_password')
def test_create_user_failure(mock_hash_password, mock_db_session):
    """Тест неудачного создания пользователя из-за не уникального логина"""
    new_user_data = schemas.UserCreate(login="nonuniqueuser", password="password123")
    with patch('app.crud.users.__is_login_unique', return_value=False):
        with pytest.raises(ValueError) as e:
            users.create_user(mock_db_session, new_user_data)
        assert str(e.value) == "Логин уже используется. Пожалуйста, выберите другой."

    mock_hash_password.assert_not_called()


@pytest.mark.parametrize("login, chat_id", [("user1", 123), ("user2", 0)])
def test_add_chat_id_by_login_success(mock_db_session, login, chat_id):
    """Тест успешного добавления chat_id"""
    mock_user = models.User(login=login)
    mock_db_session.query().filter(models.User.login == login).first.return_value = mock_user

    result = users.add_chat_id_by_login(mock_db_session, login, chat_id)
    assert result.chat_id == chat_id


def test_add_chat_id_by_login_failure(mock_db_session):
    """Тест неудачного добавления chat_id из-за отсутствия пользователя в базе"""
    login = "nonexistentuser"
    chat_id = -135
    mock_db_session.query().filter(models.User.login == login).first.return_value = None

    with pytest.raises(ValueError) as e:
        users.add_chat_id_by_login(mock_db_session, login, chat_id)
    assert str(e.value) == "Такого пользователя не существует."

    mock_db_session.commit.assert_not_called()
    mock_db_session.refresh.assert_not_called()


@patch('app.crud.users.security.verify_password')
def test_authenticate_user_success(mock_verify_password, mock_db_session):
    """Тест успешной аутентификации"""
    mock_user = models.User(login="testuser", hashed_password=pwd_context.hash("123"))
    mock_db_session.query().filter(models.User.login == "testuser").one.return_value = mock_user
    mock_verify_password.return_value = True

    authenticated_user = users.authenticate_user(mock_db_session, "testuser", "123")
    assert authenticated_user == mock_user


def test_authenticate_user_wrong_password(mock_db_session):
    """Тест неудачной аутентификации из-за неверного пароля"""
    mock_user = models.User(login="testuser", hashed_password=pwd_context.hash("correctpassword"))
    mock_db_session.query().filter(models.User.login == "testuser").one.return_value = mock_user
    with pytest.raises(ValueError) as e:
        users.authenticate_user(mock_db_session, "testuser", "wrongpassword")
    assert str(e.value) == "Неверный пароль."


def test_authenticate_user_user_not_found(mock_db_session):
    """Тест неудачной аутентификации из-за отсутствия пользователя в базе"""
    mock_db_session.query().filter(models.User.login == "nonexistentuser").one.side_effect = NoResultFound
    with pytest.raises(ValueError) as e:
        users.authenticate_user(mock_db_session, "nonexistentuser", "password123")
    assert str(e.value) == "Пользователя не существует."


def test_delete_user_success(mock_db_session):
    """Тест успешного удаления пользователя"""
    mock_user = models.User(login="user_to_delete")
    mock_db_session.query().filter(models.User.login == "user_to_delete").first.return_value = mock_user

    users.delete_user(mock_db_session, "user_to_delete")


def test_delete_user_not_found(mock_db_session):
    """Тест неудачного удаления пользователя так как его нет в базе"""
    mock_db_session.query().filter(models.User.login == "nonexistentuser").first.return_value = None

    with pytest.raises(ValueError) as e:
        users.delete_user(mock_db_session, "nonexistentuser")
    assert str(e.value) == "Пользователь не найден."

    mock_db_session.delete.assert_not_called()
    mock_db_session.commit.assert_not_called()
