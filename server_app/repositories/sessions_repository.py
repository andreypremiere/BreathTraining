from db_context.context_db_async import get_db_conn, release_db_conn
from datetime import datetime


class SessionsRepository:
    def __init__(self):
        print('Репозиторий для сессий создан')
        self.table_name = 'sessions'  # Название таблицы

    def __del__(self):
        print('Репозиторий для сессий уничтожен')

    async def create_sessions(self, procedure_id, session_data):
        """
        Создает новые сессии в базе данных на основе данных.

        :param procedure_id: UUID созданной процедуры
        :param session_data: Словарь с данными для сессий
        :return: True, если успешно, False в случае ошибки
        """
        conn = await get_db_conn()
        patient_id = session_data['patient_id']
        data = session_data['data']  # временные ряды: [[timestamp, mark_belly, mark_breast], ...]

        query = f"""
            INSERT INTO {self.table_name} (time, patient_id, procedure_id, value_1, value_2)
            VALUES ($1, $2, $3, $4, $5);
        """

        try:
            # начинаем транзакцию
            async with conn.transaction():
                # проходим по каждому элементу в data
                for item in data:
                    timestamp_str = item[0]  # временная метка в строковом формате
                    timestamp = datetime.fromisoformat(timestamp_str)  # преобразуем строку в datetime
                    mark_belly = item[1]  # значение по животу
                    mark_breast = item[2]  # значение по груди

                    # выполняем вставку
                    await conn.execute(query, timestamp, patient_id, procedure_id, mark_belly, mark_breast)

            print('Сессии успешно добавлены')
            return True
        except Exception as e:
            print(f"Ошибка при добавлении сессий: {e}")
            return False
        finally:
            await release_db_conn(conn)

    async def get_sessions_by_patient_id(self, patient_id):
        """
        Получает все сессии для пациента по его ID.

        :param patient_id: UUID пациента
        :return: Список сессий или None, если ничего не найдено
        """
        conn = await get_db_conn()

        query = f"""
            SELECT time, value_1 AS mark_belly, value_2 AS mark_breast
            FROM {self.table_name}
            WHERE patient_id = $1
            ORDER BY time DESC;
        """

        try:
            result = await conn.fetch(query, patient_id)
            if result:
                print(f"Сессии для пациента с ID {patient_id} найдены")
                return [dict(row) for row in result]
            else:
                print(f"Сессии для пациента с ID {patient_id} не найдены")
                return None
        except Exception as e:
            print(f"Ошибка при получении данных о сессиях: {e}")
            return None
        finally:
            await release_db_conn(conn)

    async def get_sessions_by_procedure_id(self, procedure_id):
        """
        Получает все сессии по ID процедуры.

        :param procedure_id: UUID процедуры
        :return: Список сессий или None, если ничего не найдено
        """
        conn = await get_db_conn()

        query = f"""
            SELECT time, value_1 AS mark_belly, value_2 AS mark_breast
            FROM {self.table_name}
            WHERE procedure_id = $1
            ORDER BY time DESC;
        """

        try:
            result = await conn.fetch(query, procedure_id)
            if result:
                print(f"Сессии для процедуры с ID {procedure_id} найдены")
                return [dict(row) for row in result]
            else:
                print(f"Сессии для процедуры с ID {procedure_id} не найдены")
                return None
        except Exception as e:
            print(f"Ошибка при получении данных о сессиях по procedure_id: {e}")
            return None
        finally:
            await release_db_conn(conn)
