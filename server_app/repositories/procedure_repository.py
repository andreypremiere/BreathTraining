from datetime import datetime

from config import Config
from db_context.context_db_async import get_db_conn, release_db_conn


class ProcedureRepository:
    def __init__(self):
        print('Репозиторий создан')
        self.table_procedures = Config.TABLE_PROCEDURES
        self.table_sessions = Config.TABLE_SESSIONS

    async def create_procedure(self, patient_id, doctor_id, created_at, timestamps, belly, breast):
        conn = None
        try:
            conn = await get_db_conn()  # Получаем соединение
            async with conn.transaction():  # Транзакция начинается
                try:
                    # Шаг 1: Добавление процедуры
                    query_procedure = f"""
                        INSERT INTO {self.table_procedures} (patient_id, doctor_id, created_at)
                        VALUES ($1, $2, $3)
                        RETURNING procedure_id;
                        """
                    result = await conn.fetchrow(query_procedure, patient_id, doctor_id, created_at)

                    # Получаем id процедуры
                    procedure_id = result['procedure_id']

                    # Шаг 2: Добавление сессий в таблицу sessions
                    query_sessions = f"""
                        INSERT INTO {self.table_sessions} (timestamp, patient_id, procedure_id, belly, breast)
                        VALUES ($1, $2, $3, $4, $5)
                        """

                    # Вставляем каждую сессию
                    for timestamp, belly_val, breast_val in zip(timestamps, belly, breast):
                        await conn.execute(query_sessions, timestamp, patient_id, procedure_id, belly_val, breast_val)

                    # Если все прошло успешно, возвращаем True
                    return True
                except Exception as e:
                    print(f"Ошибка при добавлении процедуры или сессий: {e}")
                    # Исключение вызовет автоматический откат транзакции
                    raise
        except Exception as global_error:
            print(f"Ошибка при работе с базой данных: {global_error}")
            return False
        finally:
            await release_db_conn(conn)

    async def get_procedure_by_proc_id(self, procedure_id):
        conn = None
        try:
            conn = await get_db_conn()  # Получаем соединение
            try:
                # Шаг 1: Извлечение данных из таблицы procedures
                query_procedure = f"""
                SELECT procedure_id, patient_id, doctor_id, created_at
                FROM {self.table_procedures}
                WHERE procedure_id = $1;
                """
                procedure = await conn.fetchrow(query_procedure, procedure_id)

                if not procedure:
                    return None  # Если процедура не найдена, возвращаем None

                # Шаг 2: Извлечение данных из таблицы sessions
                query_sessions = f"""
                SELECT timestamp, belly, breast
                FROM {self.table_sessions}
                WHERE procedure_id = $1
                ORDER BY timestamp ASC;
                """
                sessions = await conn.fetch(query_sessions, procedure_id)

                return {"procedure_id": procedure["procedure_id"],
                        "patient_id": procedure["patient_id"],
                        "doctor_id": procedure["doctor_id"],
                        "created_at": procedure["created_at"],
                        "sessions": sessions,
                        }

            except Exception as e:
                print(f"Ошибка при извлечении данных процедуры: {e}")
                raise
        except Exception as global_error:
            print(f"Ошибка при работе с базой данных: {global_error}")
            return None
        finally:
            await release_db_conn(conn)

    async def get_procedures_by_patient_id(self, patient_id):
        """
        Метод для получения всех процедур, принадлежащих конкретному patient_id.
        Возвращает список процедур без данных из таблицы sessions.
        """
        conn = None
        try:
            # Получаем соединение с базой данных
            conn = await get_db_conn()

            # SQL-запрос для получения процедур по patient_id
            query = f"""
            SELECT procedure_id, doctor_id, created_at
            FROM {self.table_procedures}
            WHERE patient_id = $1
            ORDER BY created_at DESC;
            """

            # Выполнение запроса
            procedures = await conn.fetch(query, patient_id)

            return procedures  # Возвращаем список процедур

        except Exception as e:
            print(f"Ошибка при извлечении процедур: {e}")
            return None  # Возвращаем None в случае ошибки

        finally:
            await release_db_conn(conn)