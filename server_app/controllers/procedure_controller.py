from quart import Blueprint, jsonify, request
from mod_services.procedure_service import ProcedureService
from quart_jwt_extended import jwt_required  # если используется JWT
from quart import Response

# создаем Blueprint для работы с процедурами
procedure_bp = Blueprint('procedure', __name__, url_prefix='/procedure')
procedure_service = ProcedureService()  # экземпляр сервиса процедур


@procedure_bp.route('/create_procedure', methods=['POST'])
# @jwt_required()  # если требуется аутентификация
async def create_procedure():
    """
    Создает новую процедуру в базе данных.
    Ожидается JSON в формате:
    {
        'patient_id': 'uuid_patient',
        'doctor_id': 'uuid_doctor',
        'data': [[str(timestamp), mark_belly, mark_breast], ...]
    }
    """
    data = await request.get_json()  # получаем данные процедуры

    try:
        # вызываем метод создания процедуры и сессий
        procedure_id = await procedure_service.create_procedure(data)

        if not procedure_id:
            return jsonify({'error': 'Не удалось создать процедуру'}), 400

        return jsonify({'procedure_id': str(procedure_id)}), 200  # возвращаем ID новой процедуры
    except Exception as e:
        return jsonify({'error': f'Произошла ошибка: {str(e)}'}), 500


@procedure_bp.route('/get_procedure_by_patient_id/<uuid:patient_id>', methods=['GET'])
# @jwt_required()  # если требуется аутентификация
async def get_procedure_by_patient_id(patient_id):
    """
    Получает данные процедуры по patient_id.
    """
    try:
        # получаем данные процедуры по ID пациента
        procedure = await procedure_service.get_procedure_by_patient_id(patient_id)

        if not procedure:
            return jsonify({'error': 'Процедура не найдена для указанного пациента'}), 404

        return jsonify(procedure), 200  # возвращаем найденные данные
    except Exception as e:
        return jsonify({'error': f'Произошла ошибка: {str(e)}'}), 500


@procedure_bp.route('/get_session_data_by_procedure_id/<uuid:procedure_id>', methods=['GET'])
# @jwt_required()  # если требуется аутентификация
async def get_session_data_by_procedure_id(procedure_id):
    """
    Получает данные временного ряда для процедуры по procedure_id
    """
    try:
        # получаем данные сессий по ID процедуры
        session_data = await procedure_service.get_session_data_by_procedure_id(procedure_id)

        if not session_data:
            return jsonify({'error': 'Данные сессий не найдены для указанной процедуры'}), 404

        return jsonify(session_data), 200  # возвращаем найденные данные
    except Exception as e:
        return jsonify({'error': f'Произошла ошибка: {str(e)}'}), 500
