from quart import Blueprint, jsonify, request
from mod_services.patient_service import PatientService
from quart_jwt_extended import create_access_token, jwt_required
from quart import Response

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')
patient_service = PatientService()


@patient_bp.route('/get_all', methods=['GET'])
# @jwt_required()  # Если нужно добавить защиту маршрута с JWT
async def get_all_patients():
    patients = await patient_service.get_all_patients()
    if not patients:
        return jsonify({'error': 'No patients found'}), 404
    return jsonify(patients)  # Возвращаем JSON-ответ через Quart


@patient_bp.route('/create_patient', methods=['POST'])
async def create_patient_by_register():
    """
    Метод для регистрации пациента в системе.

    :return: Если регистрация прошла успешно - код 200, если нет - ошибка.
    """
    data = await request.get_json()  # Получаем данные пациента

    result = await patient_service.create_patient(data)

    if not result:
        return 'Ошибка создания пациента', 408

    return '', 200


@patient_bp.route('/delete_patient', methods=['POST'])
async def delete_patient():
    data = await request.get_json()

    result = await patient_service.delete_patient(data)

    if result:
        return '', 200
    else:
        return 'Ошибка удаления пациента', 408


@patient_bp.route('/login_patient', methods=['POST'])
async def login_patient():
    data = await request.get_json()  # Асинхронно получаем данные

    result = await patient_service.login_patient(data)

    if not result:
        return 'Ошибка входа', 410

    return jsonify(access_token=result), 200
