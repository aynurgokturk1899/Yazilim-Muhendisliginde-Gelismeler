from flask import Blueprint, jsonify, request
import memory_db # Hafızadaki veritabanını import et

dietitian_bp = Blueprint('dietitian_bp', __name__, url_prefix='/api/dietitian')

# YENİ EKLENEN ROTA: Yeni Diyetisyen Ekleme (POST /api/dietitian)
@dietitian_bp.route('/', methods=['POST'])
def add_dietitian():
    data = request.get_json()
    # Kayıt formundan beklenen tüm zorunlu alanlar
    required_fields = ['username', 'password', 'email', 'tc_kimlik', 'birth_date', 'gender', 'hospital', 'phone']

    if not all(field in data for field in required_fields):
        return jsonify(msg=f"Eksik veya geçersiz veri. Zorunlu alanlar: {', '.join(required_fields)}"), 400
    
    user_id = memory_db.get_next_user_id()
    
    if any(u.get('username') == data['username'] for u in memory_db.USERS.values()):
        return jsonify(msg="Bu kullanıcı adı zaten kullanımda."), 409

    # Tam alanları içeren kullanıcı oluşturma
    new_user = {
        "id": user_id,
        "username": data['username'],
        "role": "dietitian",
        "password": data['password'],
        "email": data['email'],
        "tc_kimlik": data['tc_kimlik'],
        "birth_date": data['birth_date'],
        "gender": data['gender'],
        "hospital": data['hospital'],
        "phone": data['phone']
    }
    
    memory_db.USERS[user_id] = new_user

    return jsonify(msg=f"Diyetisyen {data['username']} başarıyla eklendi.", id=user_id), 201
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

# **DÜZELTİLEN ROTA:** Onay bekleyen hastaları listeleme rotası
@dietitian_bp.route('/<int:dietitian_id>/patients/pending', methods=['GET'])
def get_pending_patients(dietitian_id):
    # Bu diyetisyenden onay bekleyen ilişkileri bul
    pending_links = [
        l for l in memory_db.LINKS 
        if l['clinician_id'] == dietitian_id and not l['is_approved']
    ]
    
    # İlişkilerden hasta bilgilerini çek
    patients = []
    for link in pending_links:
        patient = memory_db.USERS.get(link['patient_id'])
        if patient:
            patients.append({
                "id": patient["id"],
                "username": patient["username"],
                "role": patient["role"],
                "email": patient.get("email", "Bilgi Yok")
            })
            
    return jsonify(patients), 200

# Hastayı onaylama rotası
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

# Yemek çizelgesi oluşturma rotası
@dietitian_bp.route('/<int:dietitian_id>/patient/<int:patient_id>/schedule/meal', methods=['POST'])
def create_meal_schedule(dietitian_id, patient_id):
    # Önce erişim kontrolü
    if not check_dietitian_access(dietitian_id, patient_id):
        return jsonify(msg="Bu hastaya erişim izniniz yok. Lütfen hastayı onaylayın."), 403

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

# Hastanın ilaç çizelgesini görüntüleme rotası
@dietitian_bp.route('/<int:dietitian_id>/patient/<int:patient_id>/schedule/medication', methods=['GET'])
def get_patient_medication_schedule(dietitian_id, patient_id):
    # Diyetisyenin, hastanın ilaç çizelgesini görmesi
    if not check_dietitian_access(dietitian_id, patient_id):
        return jsonify(msg="Bu hastaya erişim izniniz yok. Lütfen hastayı onaylayın."), 403
        
    schedules = [
        s for s in memory_db.MED_SCHEDULES 
        if s['patient_id'] == patient_id
    ]
    return jsonify(schedules), 200