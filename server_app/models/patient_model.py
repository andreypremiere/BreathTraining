import datetime


class PatientModel:
    def __init__(self, patient_id=None, name=None, lastname=None, surname=None, email=None,
                 number_phone=None, birthdate=None, diagnosis=None, treatmentcard=None,
                 is_active=None, gender=None, doctor_id=None):
        self.patient_id: str = patient_id
        self.name: str = name
        self.lastname: str = lastname
        self.surname: str = surname
        self.email: str = email
        self.number_phone: str = number_phone

        if isinstance(birthdate, datetime.date):
            self.birthdate: datetime.date = birthdate
        elif isinstance(birthdate, str):
            self.birthdate: datetime.date = datetime.date.fromisoformat(birthdate)
        else:
            self.birthdate: datetime.date = None

        self.diagnosis: str = diagnosis
        self.treatmentcard: str = treatmentcard
        self.is_active: bool = is_active
        self.gender: str = gender
        self.doctor_id: str = doctor_id


    def to_dict(self):
        return self.__dict__