from config import Config
from db_context.context_db_async import get_db_conn, release_db_conn


class PatientRepository:
    def __init__(self):
        print('Репозиторий создан')
        self.table_name = Config.TABLE_PATIENTS

    async def create_new_patient(self, patient):
        conn = await get_db_conn()

        patient_data = patient.to_dict()

        if 'patient_id' in patient_data:
            del patient_data['patient_id']

        query = f"""
                    INSERT INTO {self.table_name} (name, lastname, surname, email,
                                                  number_phone, birthdate, diagnosis, treatmentcard,
                                                  is_active, gender, doctor_id)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11);
                """

        try:
            # Используем транзакцию для выполнения запроса
            async with conn.transaction():
                await conn.execute(query, *patient_data.values())
            print('Пациент создан')
            return True
        except Exception as e:
            print(f"Ошибка при добавлении пациента: {e}")
        finally:
            await release_db_conn(conn)

    async def get_patients_of_doctor(self, doctor_id):
        conn = await get_db_conn()

        query = f"""
            SELECT *
            FROM {self.table_name}
            WHERE doctor_id = $1;
        """

        try:
            rows = await conn.fetch(query, doctor_id)
            return rows
        finally:
            await release_db_conn(conn)

    async def get_patients_by_name(self, lastname, name, surname):
        # Подключение к базе данных
        conn = await get_db_conn()

        query = f"SELECT * FROM {self.table_name} WHERE "
        conditions = []
        params = []

        if lastname:
            conditions.append("LOWER(lastname) LIKE $1")
            params.append(f"%{lastname.lower()}%")
        if name:
            conditions.append("LOWER(name) LIKE $2")
            params.append(f"%{name.lower()}%")
        if surname:
            conditions.append("LOWER(surname) LIKE $3")
            params.append(f"%{surname.lower()}%")

        if not conditions:
            return []

        query += " AND ".join(conditions)

        try:
            # Выполнение запроса
            rows = await conn.fetch(query, *params)
            return rows
        finally:
            # Закрытие соединения или возвращение его в пул
            await release_db_conn(conn)

    async def get_patients_by_ids(self, ids):
        if not ids:
            return []

        conn = await get_db_conn()

        placeholders = ', '.join(f'${i + 1}' for i in range(len(ids)))

        query = f"SELECT * FROM {self.table_name} WHERE patient_id IN ({placeholders})"

        try:
            rows = await conn.fetch(query, *ids)
            return rows
        except Exception as e:
            print(e)
            return
        finally:
            await release_db_conn(conn)