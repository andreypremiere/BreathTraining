from sqlalchemy.util import await_only
# import asyncio
# from services import add_new_patient
from quart import Quart
from quart_jwt_extended import JWTManager
from repositories.patients_repository import PatientRepository  # Импортируем PatientRepository
from controllers.doctor_controller import doctor_bp
from controllers.patient_controller import patient_bp
# from controllers.procedure_controller import procedure_bp
from db_context.context_db_async import setup_pool, close_pool

# from services import add_new_patient

app = Quart(__name__)


@app.before_serving
async def init_pool():
    print('Пул соединений инициализирован')
    await setup_pool(app)


@app.after_serving
async def cleanup(exception=None):
    print('Пул соединений закрыт')
    await close_pool(app, exception)



app.register_blueprint(doctor_bp)
app.register_blueprint(patient_bp)
# app.register_blueprint(procedure_bp)

app.config['JWT_SECRET_KEY'] = '1111'
jwt = JWTManager(app)


# Запуск сервера
if __name__ == '__main__':
    # Запускаем добавление нового пациента
    # asyncio.run(add_new_patient())
    app.run(debug=True)

