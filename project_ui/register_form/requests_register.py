import requests
from configuration.path_urls import Urls


def register_doctor(name, lastname, email, password, is_active=False):
    if (name or lastname or email or password) is None:
        return {'error': 'Данные не заполнены', 'body': False}

    data = {
        'name': name,
        'lastname': lastname,
        'email': email,
        'hash_password': password,
        'is_active': is_active
        }

    response = requests.post(Urls.REGISTER_DOCTOR, json=data)

    if response.status_code == 200:
        print('Пользователь создан')
        # print('Ответ:', response.json())
        return {'error': None, 'body': True}
    else:
        print(f'Ошибка: {response.text}')
        return {'error': f'Ошибка: {response.text}', 'body': None}