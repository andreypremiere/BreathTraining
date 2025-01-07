from datetime import datetime

import requests

from configuration.path_urls import Urls


def get_procedures_of_patient(patient_id):
    params = {'patient_id': patient_id}

    response = requests.get(Urls.GET_PROCEDURES_OF_PATIENT, params=params)

    if response.status_code == 200:
        data = response.json()

        for i in data:
            i['created_at'] = datetime.fromisoformat(i['created_at'])

        print("Response data:", data)
        return data
    else:
        print(f'Ошибка')
        return