from flask import Blueprint, jsonify, request
from repositories.doctors_repository import DoctorRepository
from mod_services.doctor_service import DoctorService
import json
from flask_jwt_extended import create_access_token, jwt_required
from flask import Flask, Response

doctor_bp = Blueprint('doctor', __name__, url_prefix='/doctor')
doctor_service = DoctorService()


@doctor_bp.route('/get_all', methods=['GET'])
@jwt_required()
def get_all_doctors():
    doctors = doctor_service.get_all_doctors()
    print(doctors)
    json_response = json.dumps(doctors, indent=4, default=str)
    return Response(json_response, content_type="application/json")


@doctor_bp.route('/create_doctor', methods=['POST'])
def create_doctor_by_register():
    data = request.get_json()

    doctor_service.create_doctor(data)
    # print(data)
    return '', 200


@doctor_bp.route('/login_doctor', methods=['POST'])
def login_doctor():
    email = request.get_json()['email']
    # password = request.get_json()['password']

    if email is not None:
        print(request.get_json())
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200



