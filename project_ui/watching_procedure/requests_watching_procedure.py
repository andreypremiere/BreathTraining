import requests

from configuration.path_urls import Urls


def get_procedure_by_proc_id(procedure_id):
    response = requests.get(Urls.GET_PROCEDURE_BY_PROC_ID, params={"procedure_id": procedure_id})

    if response.status_code == 200:
        data = response.json()
        print("Response data:", data)
        return data
    else:
        print(f'Ошибка')
        return []