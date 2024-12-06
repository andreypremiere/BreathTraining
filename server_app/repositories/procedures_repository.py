from db_context import context_db
from config import Config
from db_context.context_db_async import get_db_conn, release_db_conn
from datetime import datetime


class ProcedureRepository:
    def __init__(self):
        print('Репозиторий для процедуры создан')
        self.table_name = Config.TABLE_PROCEDURES

    def __del__(self):
        print('Репозиторий для процедуры уничтожен')

    async def create_procedure(self, procedure):
        """
        Создает новую процедуру в базе данных.
        """
        conn = await get_db_conn()

        procedure_data = procedure.to_dict()

        # Убираем поле procedure_id, если оно есть, так как оно генерируется автоматически
        if 'procedure_id' in procedure_data:
            del procedure_data['procedure_id']

        query = f"""
            INSERT INTO {self.table_name} (patient_id, doctor_id, created_at)
            VALUES ($1, $2, $3);
        """

        try:
            async with conn.transaction():
                await conn.execute(query, *procedure_data.values())
            print('Процедура добавлена')
            return True
        except Exception as e:
            print(f"Ошибка при добавлении процедуры: {e}")
            return False
        finally:
            await release_db_conn(conn)

    async def get_procedure_by_patient_id(self, patient_id):
        """
        Получает данные о процедуре по ID пациента.
        """
        conn = await get_db_conn()

        query = f"""
            SELECT * FROM {self.table_name} WHERE patient_id = $1;
        """

        try:
            result = await conn.fetch(query, patient_id)
            if result:
                print(f"Процедуры для пациента с ID {patient_id} найдены")
                return result
            else:
                print(f"Процедуры для пациента с ID {patient_id} не найдены")
                return None
        except Exception as e:
            print(f"Ошибка при получении данных о процедуре: {e}")
            return None
        finally:
            await release_db_conn(conn)

    async def get_sessions_by_procedure_id(self, procedure_id):
        """
        Получает данные временных рядов из SessionModel по ID процедуры.
        """
        conn = await get_db_conn()

        query = f"""
            SELECT * FROM sessions WHERE procedure_id = $1;
        """

        try:
            result = await conn.fetch(query, procedure_id)
            if result:
                print(f"Временные ряды для процедуры с ID {procedure_id} найдены")
                return result
            else:
                print(f"Временные ряды для процедуры с ID {procedure_id} не найдены")
                return None
        except Exception as e:
            print(f"Ошибка при получении данных о сессиях: {e}")
            return None
        finally:
            await release_db_conn(conn)
