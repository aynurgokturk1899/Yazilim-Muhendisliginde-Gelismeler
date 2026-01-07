from flask import Flask, jsonify, request
from flask_cors import CORS
from flasgger import Swagger # Swagger kütüphanesini ekledik
import os
from models import db, User

# Blueprint'leri import et
from patient_routes1 import patient_bp
from doctor_routes1 import doctor_bp
from dietitian_routes1 import dietitian_bp

def create_app():
    app = Flask(__name__)
    CORS(app) 

    # --- Veritabanı Ayarları ---
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://admin:adminpassword@localhost:5432/saglik_db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Swagger Ayarları ---
    app.config['SWAGGER'] = {
        'title': 'Sağlık Takip API',
        'uiversion': 3
    }
    swagger = Swagger(app) # Swagger'ı başlatıyoruz

    db.init_app(app) 

    with app.app_context():
        db.create_all()

    # Blueprint'leri kaydet
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(dietitian_bp)

    @app.route('/')
    def index():
        return "Sağlık Takip API'si Çalışıyor! Dokümantasyon için: /apidocs adresine gidin."

    # Kullanıcı Listesi
    @app.route('/api/users')
    def get_users():
        """
        Sistemdeki tüm kullanıcıları listeler.
        ---
        tags:
          - Genel
        responses:
          200:
            description: Kullanıcı listesi
        """
        users = User.query.all()
        return jsonify([u.to_dict() for u in users])
    
    # Klinisyen Listesi
    @app.route('/api/clinicians', methods=['GET'])
    def get_clinicians():
        """
        Doktor ve Diyetisyenleri listeler.
        ---
        tags:
          - Genel
        responses:
          200:
            description: Doktor ve Diyetisyen listesi objesi döner.
        """
        doctors = User.query.filter_by(role='doctor').all()
        dietitians = User.query.filter_by(role='dietitian').all()
        
        return jsonify({
            'doctors': [{'id': d.id, 'username': d.username} for d in doctors],
            'dietitians': [{'id': d.id, 'username': d.username} for d in dietitians]
        }), 200
    
    # Oturum Açma
    @app.route('/api/login', methods=['POST'])
    def login():
        """
        Kullanıcı girişi yapar.
        ---
        tags:
          - Kimlik Doğrulama
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - username
                - password
                - role
              properties:
                username:
                  type: string
                  example: ahmet
                password:
                  type: string
                  example: 1234
                role:
                  type: string
                  example: patient
        responses:
          200:
            description: Giriş başarılı
          401:
            description: Hatalı şifre veya kullanıcı adı
        """
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        if not username or not password or not role:
            return jsonify(msg="Eksik bilgi."), 400
        
        user = User.query.filter_by(username=username, role=role).first()
        
        if user and user.password == password:
            return jsonify(msg="Giriş başarılı", user_id=user.id, username=user.username, role=user.role), 200
        else:
            return jsonify(msg="Kullanıcı adı veya şifre hatalı."), 401

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)