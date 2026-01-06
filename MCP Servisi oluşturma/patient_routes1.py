from flask import Blueprint, jsonify, request
from models import db, User, PatientLink, MedSchedule, MealSchedule

patient_bp = Blueprint('patient_bp', __name__, url_prefix='/api/patient')

@patient_bp.route('/', methods=['POST'])
def add_patient():
    data = request.get_json()
    
    # Kullanıcı adı kontrolü
    if User.query.filter_by(username=data['username']).first():
        return jsonify(msg="Bu kullanıcı adı zaten kullanımda."), 409

    # Yeni Hasta Oluştur
    new_user = User(
        username=data['username'],
        role="patient",
        password=data['password'],
        email=data['email'],
        tc_kimlik=data['tc_kimlik'],
        birth_date=data['birth_date'],
        gender=data['gender'],
        height=data.get('height'),
        weight=data.get('weight')
    )
    
    db.session.add(new_user)
    db.session.commit() # ID oluşması için kaydet

    # İlişkileri Kur (Link Tablosuna Ekle)
    if data.get('selected_doctor_id'):
        link = PatientLink(patient_id=new_user.id, clinician_id=int(data['selected_doctor_id']))
        db.session.add(link)

    if data.get('selected_dietitian_id'):
        link = PatientLink(patient_id=new_user.id, clinician_id=int(data['selected_dietitian_id']))
        db.session.add(link)

    db.session.commit()
    return jsonify(msg=f"Hasta {data['username']} başarıyla eklendi.", id=new_user.id), 201

@patient_bp.route('/<int:patient_id>/schedule/medication', methods=['GET'])
def get_my_medication_schedule(patient_id):
    schedules = MedSchedule.query.filter_by(patient_id=patient_id).all()
    return jsonify([s.to_dict() for s in schedules]), 200

@patient_bp.route('/<int:patient_id>/schedule/meal', methods=['GET'])
def get_my_meal_schedule(patient_id):
    schedules = MealSchedule.query.filter_by(patient_id=patient_id).all()
    return jsonify([s.to_dict() for s in schedules]), 200