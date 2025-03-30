import requests

from configuration.path_urls import Urls


def create_new_patient(patient):
    response = requests.post(Urls.CREATE_NEW_PATIENT, json=patient)

    if response.status_code == 200:
        data = response.json()
        print("Response data:", data)
        return data['patient_id']
    else:
        print(f'Ошибка')
        return None