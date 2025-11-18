from flask import Blueprint, jsonify, request
import memory_db # Hafızadaki veritabanını import et

patient_bp = Blueprint('patient_bp', __name__, url_prefix='/api/patient')

# YENİ EKLENEN ROTA: Yeni Hasta Ekleme (POST /api/patient)
@patient_bp.route('/', methods=['POST'])
def add_patient():
    data = request.get_json()
    if not data or 'id' not in data or 'name' not in data:
        return jsonify(msg="Eksik veya geçersiz veri (ID ve Name zorunludur)."), 400
    
    user_id = int(data['id'])
    
    if user_id in memory_db.USERS:
        return jsonify(msg="Bu ID zaten kullanımda."), 409

    # Basitleştirilmiş kullanıcı oluşturma
    new_user = {
        "id": user_id,
        "username": data['name'],
        "role": "patient",
        # İstemciden gelmeyen diğer hasta alanlarını boş bırakıyoruz.
    }
    
    memory_db.USERS[user_id] = new_user

    return jsonify(msg=f"Hasta {data['name']} başarıyla eklendi.", id=user_id), 201


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