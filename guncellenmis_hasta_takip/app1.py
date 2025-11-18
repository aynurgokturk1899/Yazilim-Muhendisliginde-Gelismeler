from flask import Flask, jsonify, request
from flask_cors import CORS

# Blueprint'leri import et
from patient_routes1 import patient_bp
from doctor_routes1 import doctor_bp
from dietitian_routes1 import dietitian_bp
import memory_db 

def create_app():
    """Uygulama oluşturucu (App Factory) fonksiyonu."""
    app = Flask(__name__)
    CORS(app) 

    # Blueprint'leri kaydet
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(dietitian_bp)

    @app.route('/')
    def index():
        return "Sağlık Takip API'sine hoş geldiniz! (Giriş/Kayıt Hazır)"

    # Tüm Kullanıcıları Listele
    @app.route('/api/users')
    def get_users():
        return jsonify(list(memory_db.USERS.values()))
    
    # --- KRİTİK ROTA: Doktor ve Diyetisyen Listesi (Hasta Seçimi İçin) ---
    @app.route('/api/clinicians', methods=['GET'])
    def get_clinicians():
        doctors = [u for u in memory_db.USERS.values() if u['role'] == 'doctor']
        dietitians = [u for u in memory_db.USERS.values() if u['role'] == 'dietitian']
        
        # SADECE ID VE KULLANICI ADINI DÖNDÜRME FORMATI client_app.py ile eşleşmelidir.
        return jsonify({
            'doctors': [{'id': d['id'], 'username': d['username']} for d in doctors],
            'dietitians': [{'id': d['id'], 'username': d['username']} for d in dietitians]
        }), 200 # Başarı kodunu (200) özellikle belirtiyoruz.
    
    # --- Oturum Açma (Giriş) ---
    @app.route('/api/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')

        if not username or not password or not role:
            return jsonify(msg="Kullanıcı adı, şifre ve rol zorunludur."), 400
        
        user = next((u for u in memory_db.USERS.values() 
                     if u.get('username') == username and 
                        u.get('role') == role), None)
        
        # Basit şifre kontrolü
        if user and user.get('password') == password:
            return jsonify(msg="Giriş başarılı", user_id=user['id'], username=user['username'], role=user['role']), 200
        else:
            return jsonify(msg="Kullanıcı adı veya şifre hatalı."), 401


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)