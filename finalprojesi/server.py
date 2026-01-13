# server.py (GÜNCELLENMİŞ: Yeni Endpointler ve Test Butonları Eklendi)
from flask import Flask, jsonify, request, render_template_string
import jwt
import datetime

SECRET_KEY = "super-gizli-anahtar-123" 

app = Flask(__name__)

# --- HTML ARAYÜZÜ (GÜNCELLENDİ) ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>JWT Token Test Paneli v2</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; padding: 40px; background-color: #f4f4f9; }
        .box { background: white; padding: 25px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); max-width: 700px; margin: 0 auto; }
        h2 { color: #333; border-bottom: 2px solid #007bff; padding-bottom: 15px; margin-top:0; }
        h3 { font-size: 16px; color: #555; margin-bottom: 10px; border-left: 4px solid #ddd; padding-left: 10px; }
        
        button { padding: 10px 15px; cursor: pointer; border: none; border-radius: 6px; font-size: 14px; margin-right: 8px; margin-bottom: 10px; transition: 0.2s; }
        button:hover { opacity: 0.9; transform: translateY(-1px); }
        
        .btn-login { background-color: #28a745; color: white; }
        .btn-logout { background-color: #dc3545; color: white; }
        .btn-action { background-color: #17a2b8; color: white; }
        .btn-admin { background-color: #6610f2; color: white; }
        
        #status { margin-top: 25px; padding: 15px; border-radius: 6px; background: #e9ecef; white-space: pre-wrap; font-family: monospace; border: 1px solid #ced4da; min-height: 50px; }
        .section { margin-bottom: 25px; padding-bottom: 15px; border-bottom: 1px dashed #ddd; }
    </style>
</head>
<body>
    <div class="box">
        <h2>🔐 Gelişmiş JWT Test Paneli</h2>
        
        <div class="section">
            <h3>1. Adım: Kimlik Doğrulama</h3>
            <button onclick="login()" class="btn-login">🔑 Giriş Yap (Alice)</button>
            <button onclick="logout()" class="btn-logout">🚪 Çıkış Yap (Token Sil)</button>
        </div>

        <div class="section">
            <h3>2. Adım: Temel Koruma Testi</h3>
            <button onclick="apiCall('/protected', 'GET')" class="btn-action">🔒 Gizli Yazıyı Gör</button>
        </div>

        <div>
            <h3>3. Adım: Yeni Endpoint Testleri (Eklenenler)</h3>
            <button onclick="apiCall('/api/profile', 'GET')" class="btn-action">👤 Profilimi Getir (GET)</button>
            <button onclick="sendSecureData()" class="btn-action">📝 Rapor Gönder (POST)</button>
            <button onclick="apiCall('/api/admin-only', 'GET')" class="btn-admin">🛡️ Admin Bölgesi (Yetki Testi)</button>
        </div>

        <div id="status">Sonuçlar burada görünecek...</div>
    </div>

    <script>
        let currentToken = null;
        const statusDiv = document.getElementById('status');

        // Yardımcı: Ekrana Yazma
        function log(msg, type='neutral') {
            statusDiv.innerHTML = msg;
            if(type === 'success') statusDiv.style.backgroundColor = "#d4edda";
            else if(type === 'error') statusDiv.style.backgroundColor = "#f8d7da";
            else statusDiv.style.backgroundColor = "#e2e3e5";
        }

        // 1. GİRİŞ YAP
        async function login() {
            log("Giriş yapılıyor...");
            try {
                const res = await fetch('/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username: 'alice', password: '123456' })
                });
                const data = await res.json();
                
                if (res.ok) {
                    currentToken = data.token;
                    log("✅ <b>Giriş Başarılı!</b><br>Token alındı.", 'success');
                } else {
                    log("❌ Hata: " + data.msg, 'error');
                }
            } catch (e) { log("Bağlantı Hatası: " + e, 'error'); }
        }

        // 2. GENEL API ÇAĞRISI (GET İSTEKLERİ İÇİN)
        async function apiCall(endpoint, method) {
            if (!currentToken) {
                log("⚠️ Önce giriş yapmalısınız!", 'error');
                return;
            }
            log(endpoint + " aranıyor...");

            try {
                const res = await fetch(endpoint, {
                    method: method,
                    headers: { 'Authorization': 'Bearer ' + currentToken }
                });
                const data = await res.json();
                
                if (res.ok) {
                    // JSON çıktısını güzel formatla
                    const prettyJson = JSON.stringify(data, null, 4);
                    log("🔓 <b>İşlem Başarılı!</b><pre>" + prettyJson + "</pre>", 'success');
                } else {
                    log("⛔ Erişim Reddedildi: " + data.msg, 'error');
                }
            } catch (e) { log("Hata: " + e, 'error'); }
        }

        // 3. POST İSTEĞİ (VERİ GÖNDERME)
        async function sendSecureData() {
            if (!currentToken) {
                log("⚠️ Önce giriş yapmalısınız!", 'error');
                return;
            }
            log("Veri gönderiliyor...");

            try {
                const res = await fetch('/api/secure-post', {
                    method: 'POST',
                    headers: { 
                        'Authorization': 'Bearer ' + currentToken,
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ 
                        title: 'Aylık Sağlık Raporu', 
                        content: 'Hasta değerleri normal seviyededir.' 
                    })
                });
                const data = await res.json();
                const prettyJson = JSON.stringify(data, null, 4);
                
                if (res.ok) log("✅ <b>Veri Gönderildi!</b><pre>" + prettyJson + "</pre>", 'success');
                else log("Hata: " + data.msg, 'error');
                
            } catch (e) { log("Hata: " + e, 'error'); }
        }

        function logout() {
            currentToken = null;
            log("Token silindi. Çıkış yapıldı.");
        }
    </script>
</body>
</html>
"""

# --- YARDIMCI FONKSİYONLAR ---
def generate_jwt(username):
    payload = {
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow(),
        'nbf': datetime.datetime.utcnow(),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def verify_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except Exception as e:
        return str(e)

def token_required(f):
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header: return jsonify({'msg': 'Token yok!'}), 401
        try:
            token = auth_header.split()[1]
        except: return jsonify({'msg': 'Hatalı format'}), 401
        
        res = verify_jwt(token)
        if isinstance(res, str): return jsonify({'msg': res}), 401
        return f(res, *args, **kwargs)
    decorated.__name__ = f.__name__
    return decorated

# --- ROTALAR ---

@app.route('/')
def home():
    return render_template_string(HTML_PAGE)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # Basitlik için sadece "alice" kabul ediyoruz
    if data.get('username') == "alice" and data.get('password') == "123456":
        return jsonify({'token': generate_jwt('alice')})
    return jsonify({'msg': 'Hatalı şifre'}), 401

@app.route('/protected', methods=['GET'])
@token_required
def protected(user):
    return jsonify({'msg': 'Gizli verilere ulaştınız!', 'user_info': user['user']})

# --- YENİ EKLENEN ROTALAR ---

# 1. KİŞİSEL PROFİL (GET)
@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile(user_payload):
    username = user_payload.get('user')
    return jsonify({
        'status': 'success',
        'message': f'Merhaba {username}, profil bilgilerin yüklendi.',
        'profile_data': {
            'role': 'Doktor',
            'hospital': 'Şehir Hastanesi',
            'active_patients': 12
        }
    })

# 2. GÜVENLİ VERİ GÖNDERME (POST)
@app.route('/api/secure-post', methods=['POST'])
@token_required
def submit_secure_data(user_payload):
    data = request.get_json()
    return jsonify({
        'status': 'received',
        'server_message': 'Raporunuz güvenli şekilde işlendi.',
        'sender': user_payload['user'],
        'data_received': data
    }), 201

# 3. YETKİ KONTROLÜ (ADMIN ZONE)
@app.route('/api/admin-only', methods=['GET'])
@token_required
def admin_zone(user_payload):
    username = user_payload['user']
    
    # Sadece 'alice' admin sayılıyor
    if username != 'alice':
        return jsonify({'msg': 'YETKİSİZ ERİŞİM! Sadece admin girebilir.'}), 403
        
    return jsonify({
        'msg': 'Yönetici Paneline Hoşgeldiniz!',
        'system_stats': {
            'cpu': '12%',
            'memory': '45%',
            'active_users': 1
        }
    })

if __name__ == '__main__':
    print("Gelişmiş Test Ekranı için: http://localhost:5005 adresine gidin")
    app.run(port=5005, debug=True)