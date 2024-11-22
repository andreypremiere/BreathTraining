import asyncpg
from quart import current_app
from config import Config


async def init_db_pool():
    """Функция для инициализации асинхронного пула соединений."""
    return await asyncpg.create_pool(
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        database=Config.DB_NAME,
        min_size=1,  # Минимальное количество соединений
        max_size=5   # Максимальное количество соединений
    )


async def setup_pool(app):
    """Инициализация пула при старте приложения."""
    app.config['db_pool'] = await init_db_pool()


async def close_pool(app, exception=None):
    """Закрытие пула при завершении работы приложения."""
    if 'db_pool' in app.config:
        await app.config['db_pool'].close()


async def get_db_conn():
    """Получение соединения из пула."""
    pool = current_app.config['db_pool']
    return await pool.acquire()


async def release_db_conn(conn):
    """Возвращаем соединение обратно в пул."""
    pool = current_app.config['db_pool']
    await pool.release(conn)
