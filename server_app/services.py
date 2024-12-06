import datetime

async def add_new_patient():
    """
    Добавляет нового пациента Иванова Ивана Ивановича в базу данных.
    """
    from repositories.patients_repository import PatientRepository  # Импортируем PatientRepository
    patient_repository = PatientRepository()

    # Создаем данные нового пациента
    new_patient_data = {
        "name": "Иван",
        "lastname": "Иванов",
        "surname": "Иванович",
        "hash_password": "hashed_password_here",  # Здесь нужно использовать реальный хэш пароля
        "email": "ivanov.ivan@example.com",
        "number_phone": "+70000000000",
        "birthdate": datetime.date(1990, 1, 1),  # Указываем дату рождения
        "diagnosis": "Healthy",  # Диагноз
        "treatmentcard": "Treatment card content",  # Карта лечения
        "is_active": True,
        "gender": "male"  # Пол
    }

    # Добавляем пациента в базу
    result = patient_repository.create_patient(new_patient_data)

    if result:
        print("Пациент успешно добавлен!")
    else:
        print("Ошибка при добавлении пациента.")


