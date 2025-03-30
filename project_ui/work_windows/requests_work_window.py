from datetime import datetime

import requests

from configuration.path_urls import Urls


def create_procedure(patient_id, doctor_id, data):
    data['timestamps'] = [datetime.isoformat(ts) for ts in data['timestamps']]
    data['patient_id'] = patient_id
    data['doctor_id'] = doctor_id
    print(data)
    response = requests.post(Urls.CREATE_PROCEDURE, json=data)

    if response.status_code == 200:
        # data = response.json()
        print("Response data:", response)
        return response
    else:
        print(f'Ошибка')
        return []