from quart import Blueprint, jsonify, request
from mod_services.doctor_service import DoctorService
from quart_jwt_extended import create_access_token, jwt_required
from quart import Response

from mod_services.patient_service import PatientService

patient_bp = Blueprint('patient', __name__, url_prefix='/patient')
patient_service = PatientService()


@patient_bp.route('/create_new_patient', methods=['POST'])
# @jwt_required()
async def create_new_patient():
    data = await request.get_json()
    print(data) # {'name': 'Иван', 'lastname': 'Иванов', 'email': 'johndoe2@mail.ru', 'doctor_id': '9eba381c-529f-40e9-b200-cfd7cd897485'}

    result = await patient_service.create_new_patient(data)

    if not result:
        return 'Пациент не создан', 410

    return jsonify({'patient_id': result}), 200

@patient_bp.route('/get_patients_of_doctor', methods=['GET'])
async def get_patients_of_doctor():
    doctor_id = request.args.get('doctor_id')

    # список словарей
    result = await patient_service.get_patients_of_doctor(doctor_id)

    return jsonify(result), 200

@patient_bp.route('/get_patients_by_name', methods=['POST'])
async def get_patients_by_name():
    data = await request.get_json()

    result = await patient_service.get_patients_by_name(data)

    if isinstance(result, (list, tuple, dict)):
        return jsonify(result), 200

    if not result:
        return 'Ошибка запроса', 404

    return jsonify(result), 200

@patient_bp.route('/get_patients_by_ids', methods=['POST'])
async def get_patients_by_ids():
    data = await request.get_json()

    result = await patient_service.get_patients_by_ids(data)

    if isinstance(result, (list, tuple, dict)):
        return jsonify(result), 200

    if not result:
        return 'Ошибка запроса', 404

    return jsonify(result), 200

@patient_bp.route('/get_patient_by_id', methods=['GET'])
async def get_patient_by_id():
    patient_id = request.args.get('patient_id')

    result = await patient_service.get_patient_by_id(patient_id)

    return jsonify(result), 200