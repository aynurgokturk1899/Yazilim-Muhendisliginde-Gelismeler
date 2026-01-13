from flask import Blueprint, jsonify, request
from models import db, User, PatientLink, MedSchedule, MealSchedule

doctor_bp = Blueprint('doctor_bp', __name__, url_prefix='/api/doctor')

@doctor_bp.route('/', methods=['POST'])
def add_doctor():
    """
    Yeni Doktor Kaydı Oluşturur
    ---
    tags:
      - Doktor İşlemleri
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
            email:
              type: string
            tc_kimlik:
              type: string
            hospital:
              type: string
    responses:
      201:
        description: Doktor başarıyla eklendi
    """
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify(msg="Bu kullanıcı adı kullanımda."), 409

    new_user = User(
        username=data['username'],
        role="doctor",
        password=data['password'],
        email=data['email'],
        tc_kimlik=data['tc_kimlik'],
        birth_date=data['birth_date'],
        gender=data['gender'],
        hospital=data.get('hospital'),
        phone=data.get('phone')
    )
    
    db.session.add(new_user)
    db.session.commit()
    return jsonify(msg=f"Doktor {data['username']} eklendi.", id=new_user.id), 201

@doctor_bp.route('/<int:doctor_id>/patients/approved', methods=['GET'])
def get_approved_patients(doctor_id):
    """
    Doktorun onayladığı hastaları listeler
    ---
    tags:
      - Doktor İşlemleri
    parameters:
      - name: doctor_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Onaylı hasta listesi
    """
    links = PatientLink.query.filter_by(clinician_id=doctor_id, is_approved=True).all()
    patients = []
    for link in links:
        p = User.query.get(link.patient_id)
        patients.append({"id": p.id, "username": p.username, "email": p.email})
    return jsonify(patients), 200

@doctor_bp.route('/<int:doctor_id>/patients/pending', methods=['GET'])
def get_pending_patients(doctor_id):
    """
    Onay bekleyen hasta isteklerini listeler
    ---
    tags:
      - Doktor İşlemleri
    parameters:
      - name: doctor_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Bekleyen hasta listesi
    """
    links = PatientLink.query.filter_by(clinician_id=doctor_id, is_approved=False).all()
    patients = []
    for link in links:
        p = User.query.get(link.patient_id)
        patients.append({"id": p.id, "username": p.username, "email": p.email})
    return jsonify(patients), 200

@doctor_bp.route('/<int:doctor_id>/patients/approve/<int:patient_id>', methods=['POST'])
def approve_patient(doctor_id, patient_id):
    """
    Bir hastanın eşleşme isteğini onaylar
    ---
    tags:
      - Doktor İşlemleri
    parameters:
      - name: doctor_id
        in: path
        type: integer
        required: true
      - name: patient_id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Hasta onaylandı
    """
    link = PatientLink.query.filter_by(clinician_id=doctor_id, patient_id=patient_id).first()
    if not link:
        return jsonify(msg="İstek bulunamadı."), 404
    
    link.is_approved = True
    db.session.commit()
    return jsonify(msg="Hasta onaylandı."), 200

@doctor_bp.route('/<int:doctor_id>/patient/<int:patient_id>/schedule/medication', methods=['POST'])
def create_medication_schedule(doctor_id, patient_id):
    """
    Hastaya ilaç çizelgesi oluşturur (Eskisini siler, yenisini yazar)
    ---
    tags:
      - Doktor İşlemleri
    parameters:
      - name: doctor_id
        in: path
        type: integer
        required: true
      - name: patient_id
        in: path
        type: integer
        required: true
      - name: body
        in: body
        required: true
        schema:
          type: array
          items:
            type: object
            properties:
              day:
                type: string
              medication:
                type: string
              dosage:
                type: string
              frequency:
                type: string
    responses:
      201:
        description: Çizelge oluşturuldu
    """
    link = PatientLink.query.filter_by(clinician_id=doctor_id, patient_id=patient_id, is_approved=True).first()
    if not link:
        return jsonify(msg="Yetkisiz işlem."), 403

    data = request.get_json()
    
    MedSchedule.query.filter_by(patient_id=patient_id, doctor_id=doctor_id).delete()
    
    for item in data:
        new_schedule = MedSchedule(
            patient_id=patient_id,
            doctor_id=doctor_id,
            day=item['day'],
            medication_name=item['medication'],
            dosage=item['dosage'],
            frequency=item['frequency']
        )
        db.session.add(new_schedule)
    
    db.session.commit()
    return jsonify(msg="Çizelge oluşturuldu."), 201