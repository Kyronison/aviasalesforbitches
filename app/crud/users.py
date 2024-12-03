import bcrypt
from app import models
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session


def hash_password(password) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def create_user(db: Session, login: str, password: str) -> None:
    new_user = models.User(
        login=login,
        hashed_password=hash_password(password)
    )
    db.add(new_user)
    db.commit()


def is_login_unique_first(db: Session, login: str) -> bool:
    user = db.query(models.User).filter(models.User.login == login).first()
    return user is None


def add_chat_id_by_login(db: Session, login, chat_id_to_set):
    instance = db.query(models.User).filter(models.User.login == login).first()
    if instance:
        setattr(instance, 'chat_id', chat_id_to_set)
        db.commit()
        db.refresh(instance)


def authenticate_user(db: Session, login: str, password: str) -> models.User | None:
    try:
        user = db.query(models.User).filter(models.User.login == login).one()
        if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
            return user
        else:
            return None  # Неверный пароль
    except NoResultFound:
        return None  # Пользователь не найден
    except Exception as e:
        print(f"Ошибка при аутентификации: {e}")
        return None  # Обработка других возможных ошибок
