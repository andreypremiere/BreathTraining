from datetime import datetime

from repositories.procedure_repository import ProcedureRepository


class ProcedureService:
    def __init__(self):
        print('Сервис создан')
        self.procedure_repository = ProcedureRepository()

    def __del__(self):
        print('Сервис уничтожен')

    async def create_procedure(self, data):
        try:
            patient_id = data.get('patient_id')
            doctor_id = data.get('doctor_id')
            timestamps = [datetime.fromisoformat(ts) for ts in data.get('timestamps')]
            created_at = timestamps[0]
            belly = data.get('belly')
            breast = data.get('breast')
        except Exception as e:
            print("Ошибка", e)
            return None

        return await self.procedure_repository.create_procedure(patient_id, doctor_id,
                                                                created_at, timestamps, belly, breast)

    async def get_procedure_by_proc_id(self, procedure_id):
        result = await self.procedure_repository.get_procedure_by_proc_id(procedure_id)

        try:
            result["created_at"] = result["created_at"].isoformat()
            result["timestamp"] = []
            result["belly"] = []
            result["breast"] = []
            for i in result["sessions"]:
                result["timestamp"].append(i["timestamp"].isoformat())
                result["belly"].append(int(i["belly"]))
                result["breast"].append(int(i["breast"]))
            result.pop("sessions")
        except Exception as e:
            print(e)
            return None

        return result

    async def get_procedures_by_patient_id(self, patient_id):
        procedures = await self.procedure_repository.get_procedures_by_patient_id(patient_id)

        print(procedures)
        try:
            result = [
                {
                    "procedure_id": row["procedure_id"],
                    "doctor_id": row["doctor_id"],
                    "created_at": row["created_at"].isoformat()
                }
                for row in procedures
            ]
        except Exception as e:
            print(e)
            return None
        return result
