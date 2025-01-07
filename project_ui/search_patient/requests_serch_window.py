import requests

from configuration.path_urls import Urls


def get_patients_of_doctor(doctor_id):
    params = {'doctor_id': doctor_id}

    response = requests.get(Urls.GET_PATIENTS_OF_DOCTOR, params=params)

    if response.status_code == 200:
        data = response.json()
        print("Response data:", data)
        return data
    else:
        print(f'Ошибка')
        return


def get_patients_by_name(data):
    response = requests.post(Urls.GET_PATIENTS_BY_NAME, json=data)

    if response.status_code == 200:
        data = response.json()
        print("Response data:", data)
        return data
    else:
        print(f'Ошибка')
        return

def get_patients_by_ids(data):
    print(data)
    response = requests.post(Urls.GET_PATIENTS_BY_IDS, json={'ids': data})

    if response.status_code == 200:
        data = response.json()
        print("Response data:", data)
        return data
    else:
        print(f'Ошибка')
        return []