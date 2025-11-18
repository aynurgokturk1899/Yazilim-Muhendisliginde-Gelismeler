from flask import Blueprint, jsonify, request
import memory_db # Hafızadaki veritabanını import et

doctor_bp = Blueprint('doctor_bp', __name__, url_prefix='/api/doctor')

# YENİ EKLENEN ROTA: Yeni Doktor Ekleme (POST /api/doctor)
@doctor_bp.route('/', methods=['POST'])
def add_doctor():
    data = request.get_json()
    # Kayıt formundan beklenen tüm zorunlu alanlar
    required_fields = ['username', 'password', 'email', 'tc_kimlik', 'birth_date', 'gender', 'hospital', 'phone']

    if not all(field in data for field in required_fields):
        return jsonify(msg=f"Eksik veya geçersiz veri. Zorunlu alanlar: {', '.join(required_fields)}"), 400
    
    # Yeni kullanıcı ID'sini memory_db'den al
    user_id = memory_db.get_next_user_id()
    
    if any(u.get('username') == data['username'] for u in memory_db.USERS.values()):
        return jsonify(msg="Bu kullanıcı adı zaten kullanımda."), 409

    # Tam alanları içeren kullanıcı oluşturma
    new_user = {
        "id": user_id,
        "username": data['username'],
        "role": "doctor",
        "password": data['password'],
        "email": data['email'],
        "tc_kimlik": data['tc_kimlik'],
        "birth_date": data['birth_date'],
        "gender": data['gender'],
        "hospital": data['hospital'],
        "phone": data['phone']
    }
    
    memory_db.USERS[user_id] = new_user

    return jsonify(msg=f"Doktor {data['username']} başarıyla eklendi.", id=user_id), 201
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

# Onay bekleyen hastaları listeleme rotası
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
            # İstemcide görünmesi için gerekli bilgileri ekleyelim
            patients.append({
                "id": patient["id"],
                "username": patient["username"],
                "role": patient["role"],
                "email": patient.get("email", "Bilgi Yok")
            })
            
    return jsonify(patients), 200

# Hastayı onaylama rotası
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

# İlaç çizelgesi oluşturma rotası
@doctor_bp.route('/<int:doctor_id>/patient/<int:patient_id>/schedule/medication', methods=['POST'])
def create_medication_schedule(doctor_id, patient_id):
    # Önce erişim kontrolü
    if not check_doctor_access(doctor_id, patient_id):
        return jsonify(msg="Bu hastaya erişim izniniz yok. Lütfen hastayı onaylayın."), 403

    data = request.get_json()
    
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

# Hastanın yemek çizelgesini görüntüleme rotası
@doctor_bp.route('/<int:doctor_id>/patient/<int:patient_id>/schedule/meal', methods=['GET'])
def get_patient_meal_schedule(doctor_id, patient_id):
    # Doktorun, hastanın yemek çizelgesini görmesi
    if not check_doctor_access(doctor_id, patient_id):
        return jsonify(msg="Bu hastaya erişim izniniz yok. Lütfen hastayı onaylayın."), 403
        
    schedules = [
        s for s in memory_db.MEAL_SCHEDULES 
        if s['patient_id'] == patient_id
    ]
    return jsonify(schedules), 200