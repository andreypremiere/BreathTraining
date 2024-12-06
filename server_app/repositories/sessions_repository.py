from db_context import context_db
from config import Config
from db_context.context_db_async import get_db_conn, release_db_conn
from datetime import datetime

class SessionsRepository:
    def __init__(self):
        print('Репозиторий для сессий создан')
        self.table_name = Config.TABLE_SESSIONS

    def __del__(self):
        print('Репозиторий для сессий уничтожен')

    async def create_sessions(self, session_data):
        """
        Создает новые сессии в базе данных на основе данных.
        """
        conn = await get_db_conn()

        doctor_id = session_data['doctor_id']
        patient_id = session_data['patient_id']
        data = session_data['data']

        query = f"""
            INSERT INTO {self.table_name} (time, patient_id, part_of_body, value, procedure_id)
            VALUES ($1, $2, $3, $4, $5);
        """

        try:
            # Начинаем транзакцию
            async with conn.transaction():
                # Для каждого временного ряда в data
                for item in data:
                    timestamp_str = item[0]  # Временная метка в строковом формате
                    timestamp = datetime.fromisoformat(timestamp_str)  # Преобразуем строку в datetime
                    mark_belly = item[1]  # Значение по животу
                    mark_breast = item[2]  # Значение по груди

                    # Сессии по области тела
                    await conn.execute(query, timestamp, patient_id, 'belly', mark_belly, doctor_id)
                    await conn.execute(query, timestamp, patient_id, 'breast', mark_breast, doctor_id)

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
        """
        conn = await get_db_conn()

        query = f"""
            SELECT * FROM {self.table_name} WHERE patient_id = $1;
        """

        try:
            result = await conn.fetch(query, patient_id)
            if result:
                print(f"Сессии для пациента с ID {patient_id} найдены")
                return result
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
        """
        conn = await get_db_conn()

        query = f"""
            SELECT * FROM {self.table_name} WHERE procedure_id = $1;
        """

        try:
            result = await conn.fetch(query, procedure_id)
            if result:
                print(f"Сессии для процедуры с ID {procedure_id} найдены")
                return result
            else:
                print(f"Сессии для процедуры с ID {procedure_id} не найдены")
                return None
        except Exception as e:
            print(f"Ошибка при получении данных о сессиях по procedure_id: {e}")
            return None
        finally:
            await release_db_conn(conn)
