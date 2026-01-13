from flask_sqlalchemy import SQLAlchemy

# DB nesnesini burada oluşturuyoruz
db = SQLAlchemy()

# --- Kullanıcı Tablosu (Doktor, Hasta, Diyetisyen hepsi burada) ---
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'patient', 'doctor', 'dietitian'
    email = db.Column(db.String(120), nullable=False)
    tc_kimlik = db.Column(db.String(11), nullable=False)
    birth_date = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    
    # Hasta spesifik alanlar
    height = db.Column(db.String(10), nullable=True)
    weight = db.Column(db.String(10), nullable=True)
    
    # Doktor/Diyetisyen spesifik alanlar
    hospital = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "email": self.email,
            "hospital": self.hospital
        }

# --- İlişkiler Tablosu (Hangi hasta kime bağlı ve onay durumu) ---
class PatientLink(db.Model):
    __tablename__ = 'patient_links'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    clinician_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) # Doktor veya Diyetisyen ID
    is_approved = db.Column(db.Boolean, default=False)

    patient = db.relationship('User', foreign_keys=[patient_id], backref='clinician_links')
    clinician = db.relationship('User', foreign_keys=[clinician_id], backref='patient_requests')

# --- İlaç Çizelgesi ---
class MedSchedule(db.Model):
    __tablename__ = 'med_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    day = db.Column(db.String(20))
    medication_name = db.Column(db.String(100))
    dosage = db.Column(db.String(50))
    frequency = db.Column(db.String(50))

    def to_dict(self):
        return {
            "day": self.day,
            "medication_name": self.medication_name,
            "dosage": self.dosage,
            "frequency": self.frequency
        }

# --- Yemek Çizelgesi ---
class MealSchedule(db.Model):
    __tablename__ = 'meal_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    dietitian_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    day = db.Column(db.String(20))
    meal_name = db.Column(db.String(50))
    portion = db.Column(db.String(200))

    def to_dict(self):
        return {
            "day": self.day,
            "meal_name": self.meal_name,
            "portion": self.portion
        }