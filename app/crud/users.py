# app/crud/users.py
from app import models, schemas
from app.utils import security
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session


def __is_login_unique(db: Session, login: str) -> bool:
    """
    Проверка уникальности логина. Локальная функция

    :param db: актуальная сессия
    :param login: логин пользователя (строка)
    :return: уникальность (bool)
    """
    user = db.query(models.User).filter(models.User.login == login).first()
    return user is None


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """
    Добавление нового пользователя в базу.
    
    :param db: актуальная сессия
    :param user: 
    :return: объект User
    :raises ValueError: если логин не уникален
    """""
    if not __is_login_unique(db, user.login):
        raise ValueError("Логин уже используется. Пожалуйста, выберите другой.")

    new_user = models.User(
        login=user.login,
        hashed_password=security.hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return new_user


def add_chat_id_by_login(db: Session, login: str, chat_id_to_set: int) -> models.User:
    """
    Добавление созданному пользователю уникального chat_id

    :param db: актуальная сессия
    :param login: логин пользователя (строка)
    :param chat_id_to_set: чат id (int)
    :return: пользователя
    """
    instance = db.query(models.User).filter(models.User.login == login).first()
    if instance:
        setattr(instance, 'chat_id', chat_id_to_set)
        db.commit()
        db.refresh(instance)
        return instance
    else:
        raise ValueError("Такого пользователя не существует.")


def authenticate_user(db: Session, login: str, password: str) -> models.User | None:
    """
    Аутентификация пользователя (когда он уже существует).

    :param db: актуальная сессия
    :param login: логин пользователя (строка)
    :param password: пароль пользователя (строка)
    :return: объект User
    :raises ValueError: если логина нет в базе (пользователя не существует)
    :raises ValueError: если пароль не подходит
    :raises ValueError: какая-то другая ошибка
    """
    try:
        user = db.query(models.User).filter(models.User.login == login).one()
        if security.verify_password(password, user.hashed_password):
            return user
        else:
            raise ValueError("Неверный пароль.")
    except NoResultFound:
        raise ValueError("Пользователя не существует.")
    except Exception as e:
        raise ValueError(f"Ошибка при аутентификации: {e}")


def delete_user(db: Session, login: str) -> None:
    """
    Удаляет аккаунт пользоваателя и все его карточки по его логину

    :param db: актуальная сессия
    :param login: логин пользователя (строка)
    :return: None
    :raise Value error: если пользователь не найден
    """
    user = db.query(models.User).filter(models.User.login == login).first()
    if not user:
        return None
        # raise ValueError("Пользователь не найден.")
    db.delete(user)
    db.commit()
