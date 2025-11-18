from flask import Blueprint, jsonify, request
import memory_db

dietitian_bp = Blueprint('dietitian_bp', __name__, url_prefix='/api/dietitian')

# YENİ EKLENEN ROTA: Yeni Diyetisyen Ekleme (POST /api/dietitian)
@dietitian_bp.route('/', methods=['POST'])
def add_dietitian():
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
        "role": "dietitian",
        # Diğer diyetisyen alanlarını boş bırakıyoruz.
    }
    
    memory_db.USERS[user_id] = new_user

    return jsonify(msg=f"Diyetisyen {data['name']} başarıyla eklendi.", id=user_id), 201
# --- Yeni Rota Ekleme Sonu ---


# Basit erişim kontrolü
def check_dietitian_access(dietitian_id, patient_id):
    """Diyetisyenin bu hastaya onaylı erişimi var mı?"""
    link = next(
        (l for l in memory_db.LINKS 
         if l['patient_id'] == patient_id and 
            l['clinician_id'] == dietitian_id and 
            l['is_approved']), 
        None
    )
    return link is not None

@dietitian_bp.route('/<int:dietitian_id>/patients/pending', methods=['GET'])
def get_pending_patients(dietitian_id):
    # Bu diyetisyenden onay bekleyen ilişkileri bul
    pending_links = [
        l for l in memory_db.LINKS 
        if l['clinician_id'] == dietitian_id and not l['is_approved']
    ]
    
    patients = []
    for link in pending_links:
        patient = memory_db.USERS.get(link['patient_id'])
        if patient:
            patients.append(patient)
            
    return jsonify(patients), 200

@dietitian_bp.route('/<int:dietitian_id>/patients/approve/<int:patient_id>', methods=['POST'])
def approve_patient(dietitian_id, patient_id):
    # İlgili onay isteğini bul
    link = next(
        (l for l in memory_db.LINKS 
         if l['patient_id'] == patient_id and 
            l['clinician_id'] == dietitian_id), 
        None
    )
    
    if not link:
        return jsonify(msg="Onay isteği bulunamadı."), 404
        
    link['is_approved'] = True
    return jsonify(msg="Hasta başarıyla onaylandı."), 200

@dietitian_bp.route('/<int:dietitian_id>/patient/<int:patient_id>/schedule/meal', methods=['POST'])
def create_meal_schedule(dietitian_id, patient_id):
    if not check_dietitian_access(dietitian_id, patient_id):
        return jsonify(msg="Bu hastaya erişim izniniz yok."), 403

    data = request.get_json()
    
    # Bu hastanın mevcut yemek çizelgesini temizle
    memory_db.MEAL_SCHEDULES[:] = [
        s for s in memory_db.MEAL_SCHEDULES 
        if s['patient_id'] != patient_id or s['dietitian_id'] != dietitian_id
    ]
    
    # Yeni çizelgeyi ekle
    try:
        for item in data:
            new_schedule = {
                "id": memory_db.get_next_meal_id(),
                "patient_id": patient_id,
                "dietitian_id": dietitian_id,
                "day": item['day'],
                "meal_name": item['meal'],
                "portion": item['portion']
            }
            memory_db.MEAL_SCHEDULES.append(new_schedule)
        
        return jsonify(msg="Yemek çizelgesi başarıyla oluşturuldu."), 201
    except Exception as e:
        return jsonify(msg="Hata oluştu", error=str(e)), 500

@dietitian_bp.route('/<int:dietitian_id>/patient/<int:patient_id>/schedule/medication', methods=['GET'])
def get_patient_medication_schedule(dietitian_id, patient_id):
    # Diyetisyenin, hastanın ilaç çizelgesini görmesi
    if not check_dietitian_access(dietitian_id, patient_id):
        return jsonify(msg="Bu hastaya erişim izniniz yok."), 403
        
    schedules = [
        s for s in memory_db.MED_SCHEDULES 
        if s['patient_id'] == patient_id
    ]
    return jsonify(schedules), 200