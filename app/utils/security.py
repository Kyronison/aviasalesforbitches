import bcrypt


def hash_password(password) -> str:
    """
    Выполняется хеширование пароля

    :param password: оригинальный пароль (строка)
    :return: хешированный пароль (строка)
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Сопоставление введенного пароля хешированному паролю из базы

    :param password: введенный пароль (строка)
    :param password: пароль из бд (строка)
    :return: равенство (bool)
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))