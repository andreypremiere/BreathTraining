from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import psycopg2
import bcrypt
from config import Config
from controllers.doctor_controller import doctor_bp

app = Flask(__name__)

app.register_blueprint(doctor_bp)

# Запуск сервера
if __name__ == '__main__':
    app.run(debug=True)