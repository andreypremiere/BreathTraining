from repositories.doctors_repository import DoctorRepository
from models.doctor_model import DoctorModel


class DoctorService:
    def __init__(self):
        self.doctor_repository = DoctorRepository()

    def get_all_doctors(self):
        rows = self.doctor_repository.get_all_doctors()

        if len(rows) == 0:
            return {}

        def convert_to_dict(doctor_data):
            doctor = DoctorModel(*doctor_data)
            return doctor.to_dict()

        doctors = [convert_to_dict(doctor_data) for doctor_data in rows]

        return doctors

    def create_doctor(self, data):
        doctor = None
        try:
            doctor = DoctorModel(**data)
        except Exception as e:
            print("Ошибка создания модели")
            return False

        self.doctor_repository.create_doctor(doctor)


