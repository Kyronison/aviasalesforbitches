import pytest
from flask import url_for
from app import models, schemas
from app.crud import users, cards
import time
from unittest.mock import patch
from bs4 import BeautifulSoup


# тест тимы
# def test_login_errors(app):
#     with app.test_client() as client:
#         # Тест с неверным логином или паролем (мокируем ошибку)
#         with patch('app.crud.users.authenticate_user') as mock_authenticate_user:
#             mock_authenticate_user.side_effect = ValueError("Неверный логин или пароль")
#             response = client.post("/auth/login", data={
#                 "username": "testuser",
#                 "password": "wrongpassword"
#             })
#             assert response.status_code == 200
#             soup = BeautifulSoup(response.data, 'html.parser')
#             error_message = soup.select_one('div.error-message.error') #изменил на select_one
#             assert error_message and "Неверный логин или пароль" in error_message.text


def test_user_registration_errors(app):
    with app.test_client() as client:
        # Тест с несовпадающими паролями
        response = client.post("/auth/signup", data={
            "login": "testuser",
            "password": "securepassword",
            "password_confirm": "wrongpassword"
        })
        assert response.status_code == 200
        soup = BeautifulSoup(response.data, 'html.parser')
        error_message = soup.select_one('div.error-message.error')
        assert error_message and "Пароли не совпадают" in error_message.text

        # Тест с существующим пользователем (мокируем ошибку)
        with patch('app.crud.users.create_user') as mock_create_user:
            mock_create_user.side_effect = ValueError("Логин уже используется")
            response = client.post("/auth/signup", data={
                "login": "testuser",
                "password": "securepassword",
                "password_confirm": "securepassword"
            })
            assert response.status_code == 200
            soup = BeautifulSoup(response.data, 'html.parser')
            error_message = soup.select_one('div.error-message.error')
            assert error_message and "Логин уже используется" in error_message.text

        # Тест с успешной регистрацией (после ошибки)
        with patch('app.crud.users.create_user') as mock_create_user:
            mock_create_user.return_message = "Регистрация прошла успешно"
            mock_create_user.return_value = models.User(login="testuser2", hashed_password="some_fake_hash")
            response = client.post("/auth/signup", data={
                "login": "testuser2",
                "password": "securepassword",
                "password_confirm": "securepassword"
            })
            assert response.status_code == 302
            assert response.location == url_for('main.telegram', _external=True)