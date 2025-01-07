class Urls:
    base_host = 'http://127.0.0.1:5000'
    """
    Хранит константы url для запросов.
    """
    LOGIN_DOCTOR = f'{base_host}/doctor/login_doctor'
    REGISTER_DOCTOR = f'{base_host}/doctor/create_doctor'
    GET_PATIENTS_OF_DOCTOR = f'{base_host}/patient/get_patients_of_doctor'
    GET_PATIENTS_BY_NAME = f'{base_host}/patient/get_patients_by_name'
    GET_PATIENTS_BY_IDS = f'{base_host}/patient/get_patients_by_ids'
    CREATE_PROCEDURE = f'{base_host}/procedure/create_procedure'
    GET_PROCEDURES_OF_PATIENT = f'{base_host}/procedure/get_procedures_by_patient_id'
