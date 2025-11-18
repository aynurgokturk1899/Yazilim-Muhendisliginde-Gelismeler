from flask import Blueprint, jsonify, request
import memory_db # Hafızadaki veritabanını import et

doctor_bp = Blueprint('doctor_bp', __name__, url_prefix='/api/doctor')

# YENİ EKLENEN ROTA: Yeni Doktor Ekleme (POST /api/doctor)
@doctor_bp.route('/', methods=['POST'])
def add_doctor():
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
        "role": "doctor",
        # Diğer doktor alanlarını boş bırakıyoruz.
    }
    
    memory_db.USERS[user_id] = new_user

    return jsonify(msg=f"Doktor {data['name']} başarıyla eklendi.", id=user_id), 201
# --- Yeni Rota Ekleme Sonu ---

# Basit erişim kontrolü (Auth olmadığı için)
def check_doctor_access(doctor_id, patient_id):
    """Doktorun bu hastaya onaylı erişimi var mı?"""
    link = next(
        (l for l in memory_db.LINKS 
         if l['patient_id'] == patient_id and 
            l['clinician_id'] == doctor_id and 
            l['is_approved']), 
        None
    )
    return link is not None

@doctor_bp.route('/<int:doctor_id>/patients/pending', methods=['GET'])
def get_pending_patients(doctor_id):
    # Bu doktordan onay bekleyen ilişkileri bul
    pending_links = [
        l for l in memory_db.LINKS 
        if l['clinician_id'] == doctor_id and not l['is_approved']
    ]
    
    # İlişkilerden hasta bilgilerini çek
    patients = []
    for link in pending_links:
        patient = memory_db.USERS.get(link['patient_id'])
        if patient:
            patients.append(patient)
            
    return jsonify(patients), 200

@doctor_bp.route('/<int:doctor_id>/patients/approve/<int:patient_id>', methods=['POST'])
def approve_patient(doctor_id, patient_id):
    # İlgili onay isteğini bul
    link = next(
        (l for l in memory_db.LINKS 
         if l['patient_id'] == patient_id and 
            l['clinician_id'] == doctor_id), 
        None
    )
    
    if not link:
        return jsonify(msg="Onay isteği bulunamadı."), 404
        
    link['is_approved'] = True
    return jsonify(msg="Hasta başarıyla onaylandı."), 200

@doctor_bp.route('/<int:doctor_id>/patient/<int:patient_id>/schedule/medication', methods=['POST'])
def create_medication_schedule(doctor_id, patient_id):
    # Önce erişim kontrolü
    if not check_doctor_access(doctor_id, patient_id):
        return jsonify(msg="Bu hastaya erişim izniniz yok."), 403

    data = request.get_json()
    
    # (data bir liste olmalı: [{"day": "Pazartesi", "medication": "İlaç A", ...}, ...])
    
    # Bu hastanın mevcut ilaç çizelgesini temizle
    memory_db.MED_SCHEDULES[:] = [
        s for s in memory_db.MED_SCHEDULES 
        if s['patient_id'] != patient_id or s['doctor_id'] != doctor_id
    ]
    
    # Yeni çizelgeyi ekle
    try:
        for item in data:
            new_schedule = {
                "id": memory_db.get_next_med_id(),
                "patient_id": patient_id,
                "doctor_id": doctor_id,
                "day": item['day'],
                "medication_name": item['medication'],
                "dosage": item['dosage'],
                "frequency": item['frequency']
            }
            memory_db.MED_SCHEDULES.append(new_schedule)
        
        return jsonify(msg="İlaç çizelgesi başarıyla oluşturuldu."), 201
    except Exception as e:
        return jsonify(msg="Hata oluştu", error=str(e)), 500

@doctor_bp.route('/<int:doctor_id>/patient/<int:patient_id>/schedule/meal', methods=['GET'])
def get_patient_meal_schedule(doctor_id, patient_id):
    # Doktorun, hastanın yemek çizelgesini görmesi
    if not check_doctor_access(doctor_id, patient_id):
        return jsonify(msg="Bu hastaya erişim izniniz yok."), 403
        
    schedules = [
        s for s in memory_db.MEAL_SCHEDULES 
        if s['patient_id'] == patient_id
    ]
    return jsonify(schedules), 200