import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from config import Config


class PatientModel:
    def __init__(
        self, patient_id=None, name=None, lastname=None, surname=None, hash_password=None, email=None, number_phone=None,
        birthdate=None, diagnosis=None, treatmentcard=None, is_active=False, gender=None,
    ):
        self.patient_id: str = patient_id
        self.name: str = name
        self.lastname: str = lastname
        self.surname: str = surname
        self.hash_password: str = hash_password
        self.email: str = email
        self.number_phone: str = number_phone
        self.birthdate: datetime.date = birthdate
        self.diagnosis: str = diagnosis
        self.treatmentcard: bytes = treatmentcard
        self.is_active: bool = is_active
        self.gender: str = gender

    def to_dict(self):
        """
        Преобразует объект пациента в словарь.
        """
        return self.__dict__
