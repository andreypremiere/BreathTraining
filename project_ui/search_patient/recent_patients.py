import json


class RecentPatients:
    def __init__(self, file_path="search_patient/recent_patients.json", max_ids=20):
        """
        Инициализация менеджера ID пользователей.

        :param file_path: Путь к файлу для хранения ID.
        :param max_ids: Максимальное количество ID, которое может быть в файле.
        """
        self.file_path = file_path
        self.max_ids = max_ids
        self.recent_patients = self._load_ids()
        print(self.recent_patients)

    def _load_ids(self):
        """
        Загружает список ID из файла.

        :return: Список ID пользователей.
        """
        try:
            with open(self.file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(e)
            return []

    def _save_ids(self, ids):
        """
        Сохраняет список ID в файл.

        :param ids: Список ID для сохранения.
        """
        with open(self.file_path, 'w') as file:
            json.dump(ids, file, indent=4)

    def add_user_id(self, user_id):
        """
        Добавляет новый ID пользователя в файл.
        Удаляет старые ID, если их больше, чем max_ids.

        :param user_id: ID пользователя для добавления.
        """
        ids = self._load_ids()

        # Удалить старый ID, если он существует
        if user_id in ids:
            ids.remove(user_id)

        # Добавить новый ID в конец списка
        ids.append(user_id)

        # Оставить только последние max_ids записей
        if len(ids) > self.max_ids:
            ids = ids[-self.max_ids:]

        # Сохранить обновленный список
        self._save_ids(ids)

    def get_all_ids(self):
        """
        Получает список всех ID, сохраненных в файле.

        :return: Список ID.
        """
        return self._load_ids()


# # Пример использования
# if __name__ == "__main__":
#     manager = RecentPatients()
#
#     manager.add_user_id("2489965a-d1d6-42db-9be2-38c745d1a830")
#     manager.add_user_id("766c9c66-1872-4135-9571-3a8c14a48b70")  # Повторное добавление

