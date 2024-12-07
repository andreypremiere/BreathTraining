import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, NUMERIC
from config import Config

# инициализация SQLAlchemy
db = SQLAlchemy()

class SessionModel:
    def __init__(self, time=None, patient_id=None, part_of_body=None, value=None, procedure_id=None):
        self.time: datetime.datetime = time
        self.patient_id: str = patient_id
        self.part_of_body: str = part_of_body
        self.value: float = value
        self.procedure_id: str = procedure_id

    def to_dict(self):
        return self.__dict__

# SQLAlchemy модель для работы с таблицей sessions
class Session(db.Model):
    __tablename__ = 'sessions'  # название таблицы в базе данных

    time = db.Column(db.DateTime(timezone=True), primary_key=True, nullable=False)  # временная метка
    patient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('patients.patient_id', ondelete='CASCADE'), nullable=False)
    part_of_body = db.Column(db.String, nullable=False)  # часть тела
    value = db.Column(NUMERIC(20, 10), nullable=False)  # значение, с точностью до 10 знаков
    procedure_id = db.Column(UUID(as_uuid=True), db.ForeignKey('procedures.procedure_id', ondelete='CASCADE'), nullable=False)

    patient = db.relationship("Patient", backref="sessions", lazy=True)
    procedure = db.relationship("Procedure", backref="sessions", lazy=True)

    def __init__(self, time, patient_id, part_of_body, value, procedure_id):
        self.time = time
        self.patient_id = patient_id
        self.part_of_body = part_of_body
        self.value = value
        self.procedure_id = procedure_id

    def to_dict(self):
        return {
            "time": self.time.isoformat(),
            "patient_id": str(self.patient_id),
            "part_of_body": self.part_of_body,
            "value": str(self.value),
            "procedure_id": str(self.procedure_id)
        }
