class Config:
    SECRET_KEY = '111111111111'  # Секретный ключ для JWT
    DB_HOST = 'localhost'  # Адрес базы данных
    DB_PORT = 5432         # Порт базы данных
    DB_NAME = 'breath_training'  # Имя базы данных
    DB_USER = 'postgres'  # Пользователь базы данных
    DB_PASSWORD = '1111'  # Пароль к базе данных
    DB_OPTIONS = "-c client_encoding=UTF8"
    TABLE_DOCTORS = 'doctors'
    TABLE_PATIENTS = 'patients'
    TABLE_SESSIONS = 'sessions'
    TABLE_PROCEDURES = 'procedures'
