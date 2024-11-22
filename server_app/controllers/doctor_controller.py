from quart import Blueprint, jsonify, request
from mod_services.doctor_service import DoctorService
from quart_jwt_extended import create_access_token, jwt_required
from quart import Response

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')
doctor_service = DoctorService()


@doctor_bp.route('/get_all', methods=['GET'])
# @jwt_required()  # Если нужно добавить защиту маршрута с JWT
async def get_all_doctors():
    doctors = await doctor_service.get_all_doctors()
    # if not doctors:
    #     return jsonify({'error': 'No doctors found'}), 404
    return jsonify(doctors)  # Возвращаем JSON-ответ через Quart


@doctor_bp.route('/create_doctor', methods=['POST'])
async def create_doctor_by_register():
    """
    Метод для регистрации доктора в системе.

    :return: Если регистрация прошла успешно - код 200, если нет - .
    """
    data = await request.get_json()  # возрвщает словарь

    result = await doctor_service.create_doctor(data)

    if not result:
        return 'Ошибка создания доктора', 408

    return '', 200


@doctor_bp.route('/delete_doctor', methods=['POST'])
async def delete_doctor():
    data = await request.get_json()

    result = await doctor_service.delete_doctor(data)

    if result:
        return '', 200
    else:
        return 'Ошибка удаления доктора', 408


@doctor_bp.route('/login_doctor', methods=['POST'])
async def login_doctor():
    data = await request.get_json()  # Асинхронно получаем данные

    result = await doctor_service.login_doctor(data)

    if not result:
        return 'Ошибка входа', 410

    return jsonify(access_token=result), 200




