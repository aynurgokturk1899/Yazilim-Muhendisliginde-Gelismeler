from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from models import db, User # Modelleri import et

# Blueprint'leri import et
from patient_routes1 import patient_bp
from doctor_routes1 import doctor_bp
from dietitian_routes1 import dietitian_bp

def create_app():
    app = Flask(__name__)
    CORS(app) 

    # --- Veritabanı Ayarları ---
    # docker-compose'dan gelen DATABASE_URL çevresel değişkenini al
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://admin:adminpassword@localhost:5432/saglik_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app) # DB'yi başlat

    # Uygulama başlarken tabloları oluştur (varsa oluşturmaz)
    with app.app_context():
        db.create_all()

    # Blueprint'leri kaydet
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(dietitian_bp)

    @app.route('/')
    def index():
        return "Sağlık Takip API'si (PostgreSQL) Çalışıyor!"

    # Kullanıcı Listesi
    @app.route('/api/users')
    def get_users():
        users = User.query.all()
        return jsonify([u.to_dict() for u in users])
    
    # Klinisyen Listesi (Doktor ve Diyetisyenler)
    @app.route('/api/clinicians', methods=['GET'])
    def get_clinicians():
        doctors = User.query.filter_by(role='doctor').all()
        dietitians = User.query.filter_by(role='dietitian').all()
        
        return jsonify({
            'doctors': [{'id': d.id, 'username': d.username} for d in doctors],
            'dietitians': [{'id': d.id, 'username': d.username} for d in dietitians]
        }), 200
    
    # Oturum Açma
    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        if not username or not password or not role:
            return jsonify(msg="Eksik bilgi."), 400
        
        # SQL Sorgusu ile kullanıcıyı bul
        user = User.query.filter_by(username=username, role=role).first()
        
        if user and user.password == password:
            return jsonify(msg="Giriş başarılı", user_id=user.id, username=user.username, role=user.role), 200
        else:
            return jsonify(msg="Kullanıcı adı veya şifre hatalı."), 401

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)