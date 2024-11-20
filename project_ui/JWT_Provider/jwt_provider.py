import os
from configuration.configuration import Configuration


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
                    return token if token else None
            except Exception as e:
                print(f"Ошибка при чтении токена: {e}")
                return None
        return None

    def save_token(self, token):
        """
        Сохранение токена в файл.

        Записывает переданный токен в файл для дальнейшего использования.

        :param token: Токен для сохранения.
        """
        try:
            with open(self.token_file, "w") as file:
                file.write(token)
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
