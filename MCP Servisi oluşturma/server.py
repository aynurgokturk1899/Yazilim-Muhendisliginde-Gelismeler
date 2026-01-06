# server.py (Flask API Sunucusu)
from flask import Flask, jsonify, request
import jwt
import datetime
import time

# --- Yapılandırma ---
# GÜÇLÜ VE GİZLİ BİR ANAHTAR KULLANIN!
SECRET_KEY = "super-gizli-anahtar-123" 

app = Flask(__name__)

# Basit kullanıcı veritabanı (Gerçekte DB'den çekilmeli)
USERS = {
    "alice": "123456",
    "bob": "abcdef"
}

# --- JWT Yardımcı Fonksiyonları ---

def generate_jwt(username):
    """Belirtilen kullanıcı adı için JWT token oluşturur (1 saat geçerli)."""
    payload = {
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1), # Bitiş zamanı
        'iat': datetime.datetime.utcnow(),                            # Oluşturulma zamanı
        'nbf': datetime.datetime.utcnow(),                            # Geçerlilik başlangıcı
    }
    # HS256 algoritması ile encode et
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verify_jwt(token):
    """JWT token'ı doğrular ve payload'ı döndürür."""
    try:
        # Token'ı PyJWT kullanarak decode et
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token süresi dolmuş."
    except jwt.InvalidTokenError:
        return "Geçersiz token."
    except Exception as e:
        return f"Token doğrulama hatası: {e}"


# --- Kimlik Doğrulama Dekorasyonu (Middleware) ---

def token_required(f):
    """Korumalı rotalar için Bearer Token kontrolü yapan dekoratör."""
    def decorated(*args, **kwargs):
        # 1. Authorization header'ı kontrol et
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'msg': 'Authorization header eksik.'}), 401
        
        # 2. 'Bearer ' ön ekini ve token'ı ayıkla
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != 'bearer':
                raise ValueError("Şema 'Bearer' değil.")
        except ValueError:
            return jsonify({'msg': 'Geçersiz token formatı. Kullanım: Bearer <token>'}), 401
        
        # 3. Token'ı doğrula
        verification_result = verify_jwt(token)
        if isinstance(verification_result, str):
            # Hata mesajı döndürülmüşse (süre dolması/geçersizlik)
            return jsonify({'msg': f'Token Doğrulama Hatası: {verification_result}'}), 401
        
        # 4. Payload'ı fonksiyona geçir (Kullanıcı bilgisi)
        # Fonksiyon, şimdi token_data ile birlikte çalışabilir
        return f(verification_result, *args, **kwargs)

    decorated.__name__ = f.__name__ # Flask routing için gerekli
    return decorated


# --- Rotalar ---

@app.route('/login', methods=['POST'])
def login():
    """Kullanıcı adı ve şifre kontrolü yaparak JWT token verir."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in USERS and USERS[username] == password:
        # Başarılı giriş: Yeni JWT token oluştur
        token = generate_jwt(username)
        return jsonify({
            'msg': 'Giriş başarılı, Bearer token alındı.',
            'token': token,
            'expires_in_hours': 1
        }), 200
    else:
        return jsonify({'msg': 'Kullanıcı adı veya şifre hatalı.'}), 401

@app.route('/protected', methods=['GET'])
@token_required
def protected(token_data):
    """Sadece geçerli JWT/Bearer Token ile erişilebilen korumalı rota."""
    return jsonify({
        'msg': 'Koruma başarılı! Verilere erişim sağlandı.',
        'user_info': f"Giriş Yapan Kullanıcı: {token_data.get('user')}",
        'token_expiration': f"Token Bitiş Zamanı: {datetime.datetime.fromtimestamp(token_data.get('exp'))}"
    }), 200

if __name__ == '__main__':
    print("API Sunucusu 5000 portunda başlatılıyor...")
    app.run(port=5000, debug=True)