from flask import Blueprint, jsonify, request
# from mod_services.doctor_service import DoctorService
# import json
# from flask_jwt_extended import create_access_token, jwt_required
# from flask import Response

procedure_bp = Blueprint('procedure', __name__, url_prefix='/procedure')


@procedure_bp.route('/create_procedure', methods=['POST'])
def write_procedure():
    data = request.get_json()

    print(data)
    return '', 200
