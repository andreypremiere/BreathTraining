import requests
from configuration.path_urls import Urls


def login_doctor(email, password):
    if email is None or password is None:
        return {'error': 'Данные не заполнены', 'body': None}

    data = {
        'email': email,
        'password': password
        }

    response = requests.post(Urls.LOGIN_DOCTOR, json=data)

    if response.status_code == 200:
        print('Ответ:', response.json())
        return {'error': None, 'body': response.json()['access_token']}
    else:
        print(f'Ошибка: {response.text}')
        return {'error': f'Ошибка: {response.text}', 'body': None}

