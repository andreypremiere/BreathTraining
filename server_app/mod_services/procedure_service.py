from repositories.procedure_repository import ProcedureRepository
from repositories.session_repository import SessionsRepository
from datetime import datetime


class ProcedureService:
    def __init__(self):
        self.procedure_repository = ProcedureRepository()
        self.sessions_repository = SessionsRepository()

    async def create_procedure_with_sessions(self, data):
        """
        Создает новую процедуру и соответствующие сессии в базе данных

        :param data: Данные для создания процедуры и сессий
                     Формат:
                     {
                         'patient_id': 'uuid_patient',
                         'doctor_id': 'uuid_doctor',
                         'data': [[str(timestamp), mark_belly, mark_breast], ...]
                     }
        :return: UUID процедуры, если операция успешна, иначе None
        """
        # извлечение необходимых данных
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        session_data = data.get('data')

        if not patient_id or not doctor_id or not session_data:
            print("Ошибка: отсутствуют обязательные поля в данных")
            return None

        # получаем дату из первого элемента 'data'
        try:
            created_at = datetime.fromisoformat(session_data[0][0])
        except (IndexError, ValueError) as e:
            print(f"Ошибка обработки времени: {e}")
            return None

        # создаем новую процедуру
        procedure_id = await self.procedure_repository.create_procedure(patient_id, doctor_id, created_at)

        if not procedure_id:
            print("Ошибка создания процедуры")
            return None

        # создаем записи сессий для процедуры
        session_records = []
        for record in session_data:
            try:
                time = datetime.fromisoformat(record[0])
                value_1 = record[1]
                value_2 = record[2]
                session_records.append({
                    'time': time,
                    'patient_id': patient_id,
                    'procedure_id': procedure_id,
                    'value_1': value_1,
                    'value_2': value_2,
                })
            except (IndexError, ValueError) as e:
                print(f"Ошибка обработки записи: {record}, ошибка: {e}")
                continue

        # сохраняем сессии в базе данных
        session_result = await self.sessions_repository.create_sessions(session_records)
        if not session_result:
            print("Ошибка сохранения сессий")
            return None

        return procedure_id

    async def get_procedure_by_patient_id(self, patient_id):
        """
        Получает информацию о процедуре по ID пациента

        :param patient_id: UUID пациента
        :return: Словарь с данными процедуры или None, если процедура не найдена
        """
        if not patient_id:
            print("Ошибка: patient_id не передан")
            return None

        # получение данных процедуры из репозитория
        procedure_data = await self.procedure_repository.get_procedure_by_patient_id(patient_id)
        if procedure_data:
            print(f"Процедура для пациента {patient_id} найдена: {procedure_data}")
        else:
            print(f"Процедура для пациента {patient_id} не найдена")
        return procedure_data

    async def get_session_data_by_procedure_id(self, procedure_id):
        """
        Получает данные временного ряда для процедуры по ID процедуры

        :param procedure_id: UUID процедуры
        :return: Список словарей с данными сессий или None, если сессии не найдены
        """
        if not procedure_id:
            print("Ошибка: procedure_id не передан")
            return None

        # получение данных сессий из репозитория
        session_data = await self.sessions_repository.get_sessions_by_procedure_id(procedure_id)
        if session_data:
            print(f"Сессии для процедуры {procedure_id} найдены: {session_data}")
        else:
            print(f"Сессии для процедуры {procedure_id} не найдены")
        return session_data