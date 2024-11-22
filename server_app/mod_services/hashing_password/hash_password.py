import bcrypt


def hash_password(password: str) -> str:
    # Генерация соли и хэширование пароля
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password.decode()


# Функция для проверки пароля
def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())