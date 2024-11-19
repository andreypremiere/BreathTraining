from repositories.doctors_repository import DoctorRepository
from models.doctor_model import DoctorModel
import requests

# dc = DoctorRepository()
#
# rows = dc.get_all_doctors()
# print(rows)



# model = DoctorModel(*('48b133ac-785c-4573-b8c9-daae5e0a4126', 'Андрей', 'Vorobev', None, '1111', 'email12', None, None, None, None, None, None, True))
#
# print(model.to_dict())

response = requests.get('http://localhost:5000/doctor/get_all')
print(response.json())