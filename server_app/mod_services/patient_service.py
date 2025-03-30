from models.patient_model import PatientModel
from repositories.patient_repository import PatientRepository


def convert_to_dict(patient_data):
    patient = PatientModel(*patient_data)
    return patient.to_dict()

class PatientService:
    def __init__(self):
        print('Сервис создан')
        self.patient_repository = PatientRepository()

    def __del__(self):
        print('Сервис уничтожен')

    async def create_new_patient(self, data):
        try:
            patient = PatientModel(**data)
        except Exception as e:
            print(f"Ошибка создания модели: {e}")
            return False

        if (patient.name or patient.lastname or patient.email or patient.doctor_id) is None:
            print(patient.to_dict())
            print('Отсутсвуют необходимые параметры')
            return False

        # if not is_valid_email(patient.email):
        #     print('Введена некорректная почта')
        #     return False

        return await self.patient_repository.create_new_patient(patient)

    async def get_patients_of_doctor(self, doctor_id):
        rows = await self.patient_repository.get_patients_of_doctor(doctor_id)

        if len(rows) == 0:
            return []

        patients = [convert_to_dict(patient_data) for patient_data in rows]

        return patients

    async def get_patients_by_name(self, data):

        try:
            lastname = data.get('lastname')
            name = data.get('name')
            surname = data.get('surname')
        except Exception as e:
            print('Неправильные данные: ', e)
            return None

        rows = await self.patient_repository.get_patients_by_name(lastname, name, surname)

        if rows is None:
            return None

        if len(rows) == 0:
            return []

        patients = [convert_to_dict(patient_data) for patient_data in rows]

        return patients

    async def get_patients_by_ids(self, data):
        ids = data['ids']
        # print(ids)

        rows = await self.patient_repository.get_patients_by_ids(ids)

        if rows is None:
            return []

        if len(rows) == 0:
            return []

        patients = [convert_to_dict(patient_data) for patient_data in rows]

        return patients

    async def get_patient_by_id(self, patient_id):
        row = await self.patient_repository.get_patient_by_id(patient_id)

        if row is None:
            return None

        patient = convert_to_dict(row)

        # print(type(patient['birthdate']))
        # print(patient['birthdate'])

        patient['birthdate'] = patient['birthdate'].isoformat()
        # print(patient['birthdate'])
        return patient
