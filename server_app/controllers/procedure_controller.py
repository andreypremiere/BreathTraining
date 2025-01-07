from quart import Blueprint, jsonify, request

from mod_services.procedure_service import ProcedureService

procedure_bp = Blueprint('procedure', __name__, url_prefix='/procedure')
procedure_service = ProcedureService()

@procedure_bp.route('/create_procedure', methods=['POST'])
async def create_procedure():
    data = await request.get_json()
    print(data)

    result = await procedure_service.create_procedure(data)

    if not result:
        return 'Ошибка создания процедуры', 408

    return '', 200


@procedure_bp.route('/get_procedure_by_proc_id', methods=['GET'])
async def get_procedure_by_proc_id():
    data = request.args.get('procedure_id')

    result = await procedure_service.get_procedure_by_proc_id(data)

    if not result:
        return 'Ошибка получения процедуры', 408

    return jsonify(result), 200

@procedure_bp.route('/get_procedures_by_patient_id', methods=['GET'])
async def get_procedures_by_patient_id():
    data = request.args.get('patient_id')

    result = await procedure_service.get_procedures_by_patient_id(data)

    if not result:
        return 'Ошибка получения процедур', 408

    return jsonify(result), 200