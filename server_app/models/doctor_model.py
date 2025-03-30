import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from config import Config


class DoctorModel:
    def __init__(self, uuid=None, name=None, lastname=None, surname=None, hash_password=None, email=None,
                 number_phone=None, birthdate=None, job_position=None, gender=None, medical_category=None,
                 licencse_num=None, is_active=None):
        self.uuid: str = uuid
        self.name: str = name
        self.lastname: str = lastname
        self.surname: str = surname
        self.hash_password: str = hash_password
        self.email: str = email
        self.number_phone: str = number_phone
        self.birthdate: datetime.date = birthdate
        self.job_position: str = job_position
        self.gender: str = gender
        self.medical_category: str = medical_category
        self.licencse_num: str = licencse_num
        self.is_active: bool = is_active

    def to_dict(self):
        return self.__dict__






