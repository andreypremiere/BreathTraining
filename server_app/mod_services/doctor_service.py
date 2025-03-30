from datetime import timedelta

from repositories.doctors_repository import DoctorRepository
from models.doctor_model import DoctorModel
from mod_services.email_validation import is_valid_email
from mod_services.hashing_password.hash_password import hash_password, check_password
from quart_jwt_extended import create_access_token, jwt_required
from quart import Response

class DoctorService:
    def __init__(self):
        print('Сервис создан')
        self.doctor_repository = DoctorRepository()

    def __del__(self):
        print('Сервис уничтожен')

    async def get_all_doctors(self):
        rows = await self.doctor_repository.get_all_doctors()

        if len(rows) == 0:
            return []

        def convert_to_dict(doctor_data):
            doctor = DoctorModel(*doctor_data)
            return doctor.to_dict()

        doctors = [convert_to_dict(doctor_data) for doctor_data in rows]

        return doctors

    async def create_doctor(self, data):
        try:
            doctor = DoctorModel(**data)
        except Exception as e:
            print(f"Ошибка создания модели: {e}")
            return False

        if (doctor.name or doctor.lastname or doctor.email or doctor.hash_password or doctor.is_active) is None:
            print(doctor.to_dict())
            print('Отсутсвуют необходимые параметры')
            return False

        if not is_valid_email(doctor.email):
            print('Введена некорректная почта')
            return False

        hash_pass = hash_password(doctor.hash_password)
        doctor.hash_password = hash_pass

        return await self.doctor_repository.create_doctor(doctor)

    async def delete_doctor(self, data):
        email = data.get('email')

        if not is_valid_email(email):
            print('Введена некорректная почта')
            return False

        return await self.doctor_repository.delete_doctor(email)

    async def login_doctor(self, data):
        try:
            email = data.get('email')
            password = data.get('password')
        except Exception as e:
            print('Ошибка парсинга данных')
            return None

        if not is_valid_email(email):
            print('Введена некорректная почта')
            return None

        result = await self.doctor_repository.get_doctor_by_email(email)

        if not result:
            print('Результат не найден')
            return None

        if not check_password(password, result.get('hash_password')):
            print('Хэш пароля не совпадает')
            return None

        token = create_access_token(identity=result.get('doctor_id'), expires_delta=timedelta(hours=12))

        return token





