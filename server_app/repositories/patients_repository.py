from db_context import context_db
from config import Config
from db_context.context_db_async import get_db_conn, release_db_conn


class PatientRepository:
    def __init__(self):
        print('Репозиторий создан')
        self.table_name = Config.TABLE_PATIENTS  # Имя таблицы берется из конфигурации

    def __del__(self):
        print('Репозиторий уничтожен')

    async def get_all_patients(self):
        """
        Возвращает всех пациентов из таблицы.
        """
        conn = await get_db_conn()
        try:
            query = f"SELECT * FROM {self.table_name};"
            result = await conn.fetch(query)
            return result
        finally:
            await release_db_conn(conn)

    async def create_patient(self, patient):
        """
        Создает нового пациента на основе данных модели.
        """
        conn = await get_db_conn()
        patient_data = patient.to_dict()

        # убираем поле patient_id, если оно есть, т.к. оно генерируется автоматически
        if 'patient_id' in patient_data:
            del patient_data['patient_id']

        query = f"""
            INSERT INTO {self.table_name} (name, lastname, surname, email, number_phone, 
                                           birthdate, diagnosis, treatmentcard, is_active, gender)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10);
        """

        try:
            async with conn.transaction():
                await conn.execute(query, *patient_data.values())
            print('Пациент добавлен')
            return True
        except Exception as e:
            print(f"Ошибка при добавлении пациента: {e}")
            return False
        finally:
            await release_db_conn(conn)

    async def delete_patient(self, email):
        """
        Удаляет пациента по email.
        """
        conn = await get_db_conn()
        query = f"DELETE FROM {self.table_name} WHERE email = $1;"

        try:
            async with conn.transaction():
                await conn.execute(query, email)
            print('Пациент удален')
            return True
        except Exception as e:
            print(f"Ошибка при удалении пациента: {e}")
            return False
        finally:
            await release_db_conn(conn)

    async def get_patient_by_email(self, email):
        """
        Возвращает пациента по email.
        """
        conn = await get_db_conn()
        query = f"SELECT * FROM {self.table_name} WHERE email = $1;"

        try:
            result = await conn.fetchrow(query, email)
            if result:
                print('Пациент найден')
                return result
            else:
                print('Пациент не найден')
                return None
        except Exception as e:
            print(f"Ошибка при получении данных пациента: {e}")
            return None
        finally:
            await release_db_conn(conn)

    async def update_patient(self, patient_id, updated_data):
        """
        Обновляет данные пациента по patient_id, исключая поле is_active.
        """
        # убираем из данных поле is_active, если оно присутствует
        if 'is_active' in updated_data:
            del updated_data['is_active']

        conn = await get_db_conn()

        # генерация SQL-запроса для обновления
        columns = ", ".join([f"{key} = ${i + 1}" for i, key in enumerate(updated_data.keys())])
        query = f"UPDATE {self.table_name} SET {columns} WHERE patient_id = ${len(updated_data) + 1};"

        try:
            async with conn.transaction():
                await conn.execute(query, *updated_data.values(), patient_id)
            print('Данные пациента обновлены')
            return True
        except Exception as e:
            print(f"Ошибка при обновлении данных пациента: {e}")
            return False
        finally:
            await release_db_conn(conn)


