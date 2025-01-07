import base64
import json
import os

import jwt

from configuration.configuration import Configuration
from flask_jwt_extended import decode_token
from datetime import datetime, timezone


class JWTProvider:
    """
    Класс для работы с JWT токеном.

    Этот класс отвечает за загрузку, сохранение и удаление JWT токена из файла. Токен используется для
    аутентификации пользователей в системе.
    """

    def __init__(self):
        """
        Инициализация объекта JWTProvider.

        Устанавливает начальное значение для токена как None и указывает путь к файлу для хранения токена.
        """
        self._token = None
        self.token_file = Configuration.TOKEN_FILE

    def load_token(self):
        """
        Загрузка токена из файла.

        Проверяет наличие файла с токеном. Если файл существует и содержит токен, то возвращает его значение.
        В случае ошибки или отсутствия токена, возвращает None.

        :return: Токен из файла или None, если токен отсутствует или произошла ошибка при его чтении.
        """
        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, "r") as file:
                    token = file.read().strip()
                    self._token = token if token else None
                    return token if token else None
            except Exception as e:
                print(f"Ошибка при чтении токена: {e}")
                return None
        return None

    def save_token(self):
        """
        Сохранение токена в файл.

        Записывает переданный токен в файл для дальнейшего использования.

        :param token: Токен для сохранения.
        """
        try:
            with open(self.token_file, "w") as file:
                file.write(self._token)
            print('Токен сохранен')
        except Exception as e:
            print(f"Ошибка при сохранении токена: {e}")

    def clear_token(self):
        """
        Удаление токена из файла.

        Если файл с токеном существует, он удаляется, очищая таким образом токен из системы.
        """
        if os.path.exists(self.token_file):
            try:
                os.remove(self.token_file)
            except Exception as e:
                print(f"Ошибка при удалении токена: {e}")

    def is_token_valid(self):
        """
        Проверяет, действителен ли токен.

        Использует поле 'exp' из токена для проверки его срока действия.
        Если токен истек или некорректен, возвращает False.

        :return: True, если токен действителен; False в противном случае.
        """
        if not self._token:
            print("Токен отсутствует.")
            return False

        try:
            # Декодирование токена без проверки подписи
            decoded_token = jwt.decode(self._token, options={"verify_signature": False})

            # Проверяем наличие поля 'exp' (времени истечения)
            exp_timestamp = decoded_token.get('exp')
            if not exp_timestamp:
                print("Поле 'exp' отсутствует в токене.")
                return False

            # Проверяем срок действия токена
            expiration_time = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            current_time = datetime.now(timezone.utc)
            if current_time < expiration_time:
                print("Токен действителен.")
                return True
            else:
                print("Срок действия токена истек.")
                return False

        except jwt.ExpiredSignatureError:
            print("Срок действия токена истек.")
        except jwt.DecodeError:
            print("Ошибка декодирования токена.")
        except Exception as e:
            print(f"Неизвестная ошибка: {e}")

        return False

    def get_id_from_token(self):
        payload_encoded = self._token.split('.')[1]
        payload_decoded = base64.urlsafe_b64decode(payload_encoded + "==")
        payload = json.loads(payload_decoded)
        return payload['identity']
