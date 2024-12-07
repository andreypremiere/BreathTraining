import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID
from config import Config

# Инициализация SQLAlchemy
db = SQLAlchemy()

class ProcedureModel:
    def __init__(self, procedure_id=None, patient_id=None, doctor_id=None, created_at=None):
        self.procedure_id: str = procedure_id
        self.patient_id: str = patient_id
        self.doctor_id: str = doctor_id
        self.created_at: datetime.datetime = created_at

    def to_dict(self):
        return self.__dict__

# SQLAlchemy модель для работы с базой данных
class Procedure(db.Model):
    __tablename__ = 'procedures'  # название таблицы в базе данных

    procedure_id = db.Column(UUID(as_uuid=True), primary_key=True, nullable=False)
    patient_id = db.Column(UUID(as_uuid=True), db.ForeignKey('patients.patient_id', ondelete='CASCADE'), nullable=False)
    doctor_id = db.Column(UUID(as_uuid=True), db.ForeignKey('doctors.doctor_id', ondelete='CASCADE'), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow, nullable=False)

    patient = db.relationship("Patient", backref="procedures", lazy=True)
    doctor = db.relationship("Doctor", backref="procedures", lazy=True)

    def __init__(self, procedure_id, patient_id, doctor_id, created_at):
        self.procedure_id = procedure_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.created_at = created_at

    def to_dict(self):
        return {
            "procedure_id": str(self.procedure_id),
            "patient_id": str(self.patient_id),
            "doctor_id": str(self.doctor_id),
            "created_at": self.created_at.isoformat()
        }
