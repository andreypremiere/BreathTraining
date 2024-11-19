import psycopg2
from config import Config

DB_CONFIG = {
    'dbname': Config.DB_NAME,
    'user': Config.DB_USER,
    'password': Config.DB_PASSWORD,
    'host': Config.DB_HOST,
    'port': Config.DB_PORT
}


def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)

        print("Подключение к базе данных установлено.")
        return conn
    except psycopg2.Error as e:
        print("Ошибка при подключении к базе данных:", e)
        return None


def close_connection(conn):
    try:
        conn.close()
        print("Подключение закрыто.")
    except psycopg2.Error as e:
        print("Ошибка при закрытии соединения: ", e)
