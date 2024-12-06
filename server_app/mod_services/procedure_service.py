from repositories.procedure_repository import ProcedureRepository  # Импорт репозитория для процедур
from repositories.session_repository import SessionsRepository  # Импорт репозитория для сессий
from datetime import datetime


class ProcedureService:
    def __init__(self):
        self.procedure_repository = ProcedureRepository()  # Экземпляр репозитория для работы с процедурами
        self.sessions_repository = SessionsRepository()  # Экземпляр репозитория для работы с сессиями

    async def create_procedure(self, data):
        """
        Создает новую процедуру в базе данных.

        :param data: Данные для создания процедуры, должны включать patient_id, doctor_id, created_at
        :return: True, если операция успешна, False в противном случае
        """
        # Получаем необходимые данные из запроса
        patient_id = data.get('patient_id')
        doctor_id = data.get('doctor_id')
        created_at = data.get('created_at', datetime.utcnow())  # Если created_at не передан, ставим текущее время

        if not patient_id or not doctor_id:
            return False  # Если нет patient_id или doctor_id, возвращаем ошибку

        # Создаем процедуру через репозиторий
        result = await self.procedure_repository.create_procedure(patient_id, doctor_id, created_at)
        return result

    async def get_procedure_by_patient_id(self, patient_id):
        """
        Получает информацию о процедуре по ID пациента.

        :param patient_id: Идентификатор пациента
        :return: Данные процедуры или None, если процедура не найдена
        """
        if not patient_id:
            return None  # Если patient_id не передан, возвращаем None

        # Получаем данные о процедуре из репозитория
        procedure_data = await self.procedure_repository.get_procedure_by_patient_id(patient_id)
        return procedure_data

    async def get_session_data_by_procedure_id(self, procedure_id):
        """
        Получает данные временного ряда для процедуры по ID процедуры.

        :param procedure_id: Идентификатор процедуры
        :return: Список с данными сессий или None, если сессии не найдены
        """
        if not procedure_id:
            return None  # Если procedure_id не передан, возвращаем None

        # Получаем данные сессий из репозитория
        session_data = await self.sessions_repository.get_sessions_by_procedure_id(procedure_id)
        return session_data
