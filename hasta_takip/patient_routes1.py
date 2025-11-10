from flask import Blueprint, jsonify
import memory_db # Hafızadaki veritabanını import et

patient_bp = Blueprint('patient_bp', __name__, url_prefix='/api/patient')

@patient_bp.route('/<int:patient_id>/schedule/medication', methods=['GET'])
def get_my_medication_schedule(patient_id):
    # İlgili hastanın tüm ilaç çizelgelerini filtrele
    schedules = [
        s for s in memory_db.MED_SCHEDULES 
        if s['patient_id'] == patient_id
    ]
    return jsonify(schedules), 200

@patient_bp.route('/<int:patient_id>/schedule/meal', methods=['GET'])
def get_my_meal_schedule(patient_id):
    # İlgili hastanın tüm yemek çizelgelerini filtrele
    schedules = [
        s for s in memory_db.MEAL_SCHEDULES 
        if s['patient_id'] == patient_id
    ]
    return jsonify(schedules), 200