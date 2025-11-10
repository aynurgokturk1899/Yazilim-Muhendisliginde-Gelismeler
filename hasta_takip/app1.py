from flask import Flask, jsonify
from flask_cors import CORS

# Blueprint'leri import et
from patient_routes1 import patient_bp
from doctor_routes1 import doctor_bp
from dietitian_routes1 import dietitian_bp
import memory_db # Kullanıcı listesi için

def create_app():
    """Uygulama oluşturucu (App Factory) fonksiyonu."""
    app = Flask(__name__)
    CORS(app) # CORS'u etkinleştir

    # Blueprint'leri kaydet
    app.register_blueprint(patient_bp)
    app.register_blueprint(doctor_bp)
    app.register_blueprint(dietitian_bp)

    @app.route('/')
    def index():
        return "Sağlık Takip API'sine hoş geldiniz! (Veritabanı ve Auth Yok)"

    # Test için kullanıcıları listeleyen basit bir endpoint
    @app.route('/api/users')
    def get_users():
        # ID'leri key olan dict'i bir listeye çevirip döndür
        return jsonify(list(memory_db.USERS.values()))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)