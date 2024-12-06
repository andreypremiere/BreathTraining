from datetime import timedelta
from repositories.patients_repository import PatientRepository
from models.patient_model import PatientModel
from mod_services.email_validation import is_valid_email
from mod_services.hashing_password.hash_password import hash_password, check_password
from quart_jwt_extended import create_access_token, jwt_required
from quart import Response


class PatientService:
    def __init__(self):
        print('Сервис создан')
        self.patient_repository = PatientRepository()

    def __del__(self):
        print('Сервис уничтожен')

    async def get_all_patients(self):
        rows = await self.patient_repository.get_all_patients()

        if len(rows) == 0:
            return {}

        def convert_to_dict(patient_data):
            patient = PatientModel(*patient_data)
            return patient.to_dict()

        patients = [convert_to_dict(patient_data) for patient_data in rows]

        return patients

    async def create_patient(self, data):
        try:
            patient = PatientModel(**data)
        except Exception as e:
            print(f"Ошибка создания модели: {e}")
            return False

        if (patient.name or patient.lastname or patient.email or patient.hash_password or patient.is_active) is None:
            print(patient.to_dict())
            print('Отсутсвуют необходимые параметры')
            return False

        if not is_valid_email(patient.email):
            print('Введена некорректная почта')
            return False

        hash_pass = hash_password(patient.hash_password)
        patient.hash_password = hash_pass

        return await self.patient_repository.create_patient(patient)

    async def delete_patient(self, data):
        email = data.get('email')

        if not is_valid_email(email):
            print('Введена некорректная почта')
            return False

        return await self.patient_repository.delete_patient(email)

    async def login_patient(self, data):
        try:
            email = data.get('email')
            password = data.get('password')
        except Exception as e:
            print('Ошибка парсинга данных')
            return None

        if not is_valid_email(email):
            print('Введена некорректная почта')
            return None

        result = await self.patient_repository.get_patient_by_email(email)

        if not result:
            print('Пациент не найден')
            return None

        if not check_password(password, result.get('hash_password')):
            print('Хэш пароля не совпадает')
            return None

        token = create_access_token(identity=email, expires_delta=timedelta(hours=12))

        return token
