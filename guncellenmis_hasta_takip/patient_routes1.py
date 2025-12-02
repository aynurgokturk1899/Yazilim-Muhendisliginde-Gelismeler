# patient_routes1.py hasta rutinleri

from flask import Blueprint, jsonify, request
import memory_db 

patient_bp = Blueprint('patient_bp', __name__, url_prefix='/api/patient')

# YENİ EKLENEN ROTA: Yeni Hasta Ekleme (POST /api/patient)
@patient_bp.route('/', methods=['POST'])
def add_patient():
    data = request.get_json()
    required_fields = ['username', 'password', 'email', 'tc_kimlik', 'birth_date', 'gender']
    
    if not all(field in data for field in required_fields):
        return jsonify(msg=f"Eksik veya geçersiz veri. Zorunlu alanlar: {', '.join(required_fields)}"), 400
    
    user_id = memory_db.get_next_user_id()
    
    if any(u.get('username') == data['username'] for u in memory_db.USERS.values()):
        return jsonify(msg="Bu kullanıcı adı zaten kullanımda."), 409

    new_user = {
        "id": user_id,
        "username": data['username'],
        "role": "patient",
        "password": data['password'],
        "email": data['email'],
        "tc_kimlik": data['tc_kimlik'],
        "birth_date": data['birth_date'],
        "gender": data['gender'],
        "height": data.get('height'),
        "weight": data.get('weight')
    }
    
    memory_db.USERS[user_id] = new_user

    # --- KRİTİK İLİŞKİLENDİRME MANTIĞI ---
    link_messages = []

    # Doktor ilişkisi
    selected_doctor_id = data.get('selected_doctor_id')
    
    # Boş string ("") kontrolü yapılır ve sadece geçerli bir değer varsa işlenir.
    if selected_doctor_id and selected_doctor_id != "":
        doctor_id = int(selected_doctor_id) 
        new_user['selected_doctor_id'] = doctor_id
        
        link = {
            "id": memory_db.get_next_link_id(),
            "patient_id": user_id,
            "clinician_id": doctor_id, 
            "is_approved": False 
        }
        memory_db.LINKS.append(link)
        link_messages.append(f"Doktor ID {doctor_id} için onay isteği gönderildi.")

    # Diyetisyen ilişkisi
    selected_dietitian_id = data.get('selected_dietitian_id')
    
    # Boş string ("") kontrolü yapılır ve sadece geçerli bir değer varsa işlenir.
    if selected_dietitian_id and selected_dietitian_id != "":
        dietitian_id = int(selected_dietitian_id)
        new_user['selected_dietitian_id'] = dietitian_id
        
        link = {
            "id": memory_db.get_next_link_id(),
            "patient_id": user_id,
            "clinician_id": dietitian_id, 
            "is_approved": False 
        }
        memory_db.LINKS.append(link)
        link_messages.append(f"Diyetisyen ID {dietitian_id} için onay isteği gönderildi.")
    # --- İLİŞKİLENDİRME MANTIĞI SONU ---

    msg = f"Hasta {data['username']} başarıyla eklendi." + (" ".join(link_messages) if link_messages else "")
    return jsonify(msg=msg, id=user_id), 201


@patient_bp.route('/<int:patient_id>/schedule/medication', methods=['GET'])
def get_my_medication_schedule(patient_id):
    schedules = [
        s for s in memory_db.MED_SCHEDULES 
        if s['patient_id'] == patient_id
    ]
    return jsonify(schedules), 200

@patient_bp.route('/<int:patient_id>/schedule/meal', methods=['GET'])
def get_my_meal_schedule(patient_id):
    schedules = [
        s for s in memory_db.MEAL_SCHEDULES 
        if s['patient_id'] == patient_id
    ]

    return jsonify(schedules), 200
