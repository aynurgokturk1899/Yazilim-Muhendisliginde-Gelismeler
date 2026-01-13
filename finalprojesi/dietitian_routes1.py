from flask import Blueprint, jsonify, request
from models import db, User, PatientLink, MealSchedule

dietitian_bp = Blueprint('dietitian_bp', __name__, url_prefix='/api/dietitian')

@dietitian_bp.route('/', methods=['POST'])
def add_dietitian():
    """
    Yeni Diyetisyen Kaydı Oluşturur
    ---
    tags:
      - Diyetisyen İşlemleri
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
    responses:
      201:
        description: Diyetisyen eklendi
    """
    data = request.get_json()
    
    if User.query.filter_by(username=data['username']).first():
        return jsonify(msg="Bu kullanıcı adı kullanımda."), 409

    new_user = User(
        username=data['username'],
        role="dietitian",
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
    return jsonify(msg=f"Diyetisyen {data['username']} eklendi.", id=new_user.id), 201

@dietitian_bp.route('/<int:dietitian_id>/patients/approved', methods=['GET'])
def get_approved_patients(dietitian_id):
    """
    Onaylı hastaları listeler
    ---
    tags:
      - Diyetisyen İşlemleri
    parameters:
      - name: dietitian_id
        in: path
        type: integer
    responses:
      200:
        description: Hasta listesi
    """
    links = PatientLink.query.filter_by(clinician_id=dietitian_id, is_approved=True).all()
    patients = []
    for link in links:
        p = User.query.get(link.patient_id)
        patients.append({"id": p.id, "username": p.username, "email": p.email})
    return jsonify(patients), 200

@dietitian_bp.route('/<int:dietitian_id>/patients/pending', methods=['GET'])
def get_pending_patients(dietitian_id):
    """
    Onay bekleyen hastaları listeler
    ---
    tags:
      - Diyetisyen İşlemleri
    parameters:
      - name: dietitian_id
        in: path
        type: integer
    responses:
      200:
        description: Bekleyen liste
    """
    links = PatientLink.query.filter_by(clinician_id=dietitian_id, is_approved=False).all()
    patients = []
    for link in links:
        p = User.query.get(link.patient_id)
        patients.append({"id": p.id, "username": p.username, "email": p.email})
    return jsonify(patients), 200

@dietitian_bp.route('/<int:dietitian_id>/patients/approve/<int:patient_id>', methods=['POST'])
def approve_patient(dietitian_id, patient_id):
    """
    Hasta isteğini onaylar
    ---
    tags:
      - Diyetisyen İşlemleri
    parameters:
      - name: dietitian_id
        in: path
        type: integer
      - name: patient_id
        in: path
        type: integer
    responses:
      200:
        description: Onaylandı
    """
    link = PatientLink.query.filter_by(clinician_id=dietitian_id, patient_id=patient_id).first()
    if not link:
        return jsonify(msg="İstek bulunamadı."), 404
    
    link.is_approved = True
    db.session.commit()
    return jsonify(msg="Hasta onaylandı."), 200

@dietitian_bp.route('/<int:dietitian_id>/patient/<int:patient_id>/schedule/meal', methods=['POST'])
def create_meal_schedule(dietitian_id, patient_id):
    """
    Hastaya beslenme programı yazar (Eskisini siler)
    ---
    tags:
      - Diyetisyen İşlemleri
    parameters:
      - name: dietitian_id
        in: path
        type: integer
      - name: patient_id
        in: path
        type: integer
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
              meal:
                type: string
              portion:
                type: string
    responses:
      201:
        description: Program kaydedildi
    """
    link = PatientLink.query.filter_by(clinician_id=dietitian_id, patient_id=patient_id, is_approved=True).first()
    if not link:
        return jsonify(msg="Yetkisiz işlem."), 403

    data = request.get_json()
    
    MealSchedule.query.filter_by(patient_id=patient_id, dietitian_id=dietitian_id).delete()
    
    for item in data:
        new_schedule = MealSchedule(
            patient_id=patient_id,
            dietitian_id=dietitian_id,
            day=item['day'],
            meal_name=item['meal'],
            portion=item['portion']
        )
        db.session.add(new_schedule)
    
    db.session.commit()
    return jsonify(msg="Çizelge oluşturuldu."), 201