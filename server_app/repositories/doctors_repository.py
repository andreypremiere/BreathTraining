from db_context import context_db
from config import Config
from db_context.context_db_async import get_db_conn, release_db_conn


class DoctorRepository:
    def __init__(self):
        print('Репозиторий создан')
        self.table_name = Config.TABLE_DOCTORS

    def __del__(self):
        print('Репозиторий уничтожен')
        # context_db.close_connection(self.conn)

    async def get_all_doctors(self):
        # Получаем соединение через get_db_conn
        conn = await get_db_conn()
        try:
            # Выполняем асинхронный запрос
            result = await conn.fetch(f"SELECT * FROM {self.table_name}")
            return result
        finally:
            # Возвращаем соединение в пул
            await release_db_conn(conn)

    async def create_doctor(self, doctor):
        conn = await get_db_conn()

        doctor_data = doctor.to_dict()

        if 'uuid' in doctor_data:
            del doctor_data['uuid']

        query = f"""
            INSERT INTO {self.table_name} (name, lastname, surname, hash_password, email,
                                          number_phone, birthdate, job_position, gender,
                                          medical_category, licencse_num, is_active)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12);
        """

        try:
            # Используем транзакцию для выполнения запроса
            async with conn.transaction():
                await conn.execute(query, *doctor_data.values())
            print('Данные добавлены')
            return True
        except Exception as e:
            print(f"Ошибка при добавлении данных: {e}")
        finally:
            await release_db_conn(conn)

    async def delete_doctor(self, email):
        conn = await get_db_conn()

        query = f'DELETE FROM {self.table_name} WHERE email = $1;'

        try:
            # Используем транзакцию для выполнения запроса
            async with conn.transaction():
                await conn.execute(query, email)
            print('Доктор удален')
            return True
        except Exception as e:
            print(f"Ошибка при удалении доктора: {e}")
        finally:
            await release_db_conn(conn)

    #
    # def delete_all_doctors(self):
    #     cursor = self.conn.cursor()
    #
    #     query = f"DELETE FROM {self.table_name}"
    #     cursor.execute(query)
    #
    #     self.conn.commit()
    #     cursor.close()
    #
    #     print("Записи успешно удалены.")

    async def get_doctor_by_email(self, email):
        conn = await get_db_conn()

        query = f'SELECT * FROM {self.table_name} WHERE email = $1;'

        try:
            # Выполняем запрос на получение записи
            result = await conn.fetchrow(query, email)
            print(result)

            if result:
                print('Доктор найден')
                return result  # Возвращаем найденную запись
            else:
                print('Доктор не найден')
                return None  # Если запись не найдена, возвращаем None
        except Exception as e:
            print(f"Ошибка при получении данных доктора: {e}")
            return None
        finally:
            # Закрываем соединение
            await release_db_conn(conn)
