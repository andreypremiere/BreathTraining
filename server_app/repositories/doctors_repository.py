from db_context import context_db
from config import Config


class DoctorRepository:
    def __init__(self):
        self.conn = context_db.get_connection()
        self.table_name = Config.TABLE_DOCTORS

    def __del__(self):
        context_db.close_connection(self.conn)

    def get_all_doctors(self):
        curs = self.conn.cursor()
        curs.execute(f"SELECT * FROM {self.table_name}")

        rows = curs.fetchall()

        curs.close()
        return rows

    def create_doctor(self, doctor):
        curs = self.conn.cursor()

        doctor_data = doctor.to_dict()

        if 'uuid' in doctor_data:
            del doctor_data['uuid']

        query = f"""
                    INSERT INTO {self.table_name} (name, lastname, surname, hash_password, email, 
                                                  number_phone, birthdate, job_position, gender, 
                                                  medical_category, licencse_num, is_active)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """

        curs.execute(query, tuple(doctor_data.values()))
        self.conn.commit()
        print('Данные добавлены')
        curs.close()

    # def delete_doctor(self, email):
    #     cursor = self.conn.cursor()
    #
    #     query = f"DELETE FROM {self.table_name} WHERE email = %s;"
    #     cursor.execute(query, (email,))
    #
    #     self.conn.commit()
    #     cursor.close()
    #
    #     print("Запись успешно удалена.")
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


