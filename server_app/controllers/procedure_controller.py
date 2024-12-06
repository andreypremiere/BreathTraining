from quart import Blueprint, jsonify, request
from mod_services.procedure_service import ProcedureService  # Импортируем сервис процедур
from quart_jwt_extended import jwt_required
from quart import Response

procedure_bp = Blueprint('procedure', __name__, url_prefix='/procedure')
procedure_service = ProcedureService()  # Экземпляр сервиса для работы с процедурами


@procedure_bp.route('/create_procedure', methods=['POST'])
# @jwt_required()  # Если нужно добавить защиту маршрута с JWT
async def create_procedure():
    """
    Создает новую процедуру в базе данных.
    Данные приходят в формате JSON:
    {
        'patient_id': 'uuid_patient',
        'doctor_id': 'uuid_doctor',
        'created_at': 'timestamp'
    }
    """
    data = await request.get_json()  # Получаем данные процедуры

    result = await procedure_service.create_procedure(data)  # Создаем процедуру с помощью сервиса

    if not result:
        return jsonify({'error': 'Ошибка создания процедуры'}), 400

    return '', 200  # Возвращаем успешный ответ


@procedure_bp.route('/get_procedure_by_patient_id/<uuid:patient_id>', methods=['GET'])
# @jwt_required()  # Если нужно добавить защиту маршрута с JWT
async def get_procedure_by_patient_id(patient_id):
    """
    Получает данные процедуры по patient_id.
    """
    procedure = await procedure_service.get_procedure_by_patient_id(patient_id)  # Получаем процедуру по ID пациента

    if not procedure:
        return jsonify({'error': 'Процедура не найдена для этого пациента'}), 404

    return jsonify(procedure), 200  # Возвращаем данные процедуры


@procedure_bp.route('/get_session_data_by_procedure_id/<uuid:procedure_id>', methods=['GET'])
# @jwt_required()  # Если нужно добавить защиту маршрута с JWT
async def get_session_data_by_procedure_id(procedure_id):
    """
    Получает данные временного ряда для процедуры по procedure_id.
    """
    session_data = await procedure_service.get_session_data_by_procedure_id(procedure_id)  # Получаем данные сессии

    if not session_data:
        return jsonify({'error': 'Данные сессий не найдены для этой процедуры'}), 404

    return jsonify(session_data), 200  # Возвращаем данные сессии
