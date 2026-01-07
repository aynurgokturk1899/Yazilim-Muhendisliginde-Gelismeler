# client_app.py (GÜNCEL ve TAM Kayıt/Giriş Merkezi, Güçlendirilmiş Hata Yönetimi ile)

from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import requests
import json

# Ana API'mizin çalıştığı adres (Docker servisi adı)
# Bu URL, Python/Flask tarafındaki POST istekleri için kullanılmaya devam etmelidir.
API_BASE_URL = "http://saglik_takip_app:5000"

app = Flask(__name__)

# --- Göz Alıcı HTML ve CSS Şablonu (Kayıt/Giriş Merkezi) ---
HTML_TEMPLATE_MAIN = """
<!doctype html>
<title>🩺 Sağlık Takip Sistemi Giriş/Kayıt</title>
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 0; }
    .container { max-width: 800px; margin: 50px auto; background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); }
    h1 { color: #007bff; text-align: center; margin-bottom: 30px; }
    h2 { color: #28a745; border-bottom: 2px solid #28a745; padding-bottom: 10px; margin-top: 20px; }
    .form-group { margin-bottom: 15px; }
    label { display: block; margin-bottom: 5px; font-weight: bold; color: #555; }
    input[type="text"], input[type="password"], input[type="email"], input[type="date"], select, textarea { 
        width: 100%; padding: 10px; border: 1px solid #ccc; border-radius: 6px; box-sizing: border-box; 
    }
    button, input[type="submit"] {
        background-color: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 6px; 
        cursor: pointer; font-size: 16px; transition: background-color 0.3s ease;
    }
    button:hover, input[type="submit"]:hover { background-color: #0056b3; }
    .message { padding: 10px; margin-bottom: 20px; border-radius: 6px; }
    .success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
    .error { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
    .menu-button { display: inline-block; margin-right: 15px; }
</style>

<div class="container">
    <h1>🏥 Sağlık Takip Sistemi Giriş/Kayıt</h1>

    {% if message %}
        <p class="message success">{{ message }}</p>
    {% endif %}
    {% if error %}
        <p class="message error">{{ error }}</p>
    {% endif %}
    {% if alert %}
        <p class="message error">{{ alert }}</p>
    {% endif %}

    <div style="text-align: center; margin-bottom: 30px;">
        <div class="menu-button"><button onclick="document.getElementById('login-form').style.display='block'; document.getElementById('register-form').style.display='none';">Giriş Yap</button></div>
        <div class="menu-button"><button onclick="document.getElementById('login-form').style.display='none'; document.getElementById('register-form').style.display='block';">Kayıt Ol</button></div>
    </div>
    
    <hr>
    
    <div id="login-form" style="display:block;">
        <h2>🔐 Giriş Yap</h2>
        <form method="POST" action="/login">
            <div class="form-group"><label for="login_role">Rol:</label><select id="login_role" name="role"><option value="patient">Hasta</option><option value="doctor">Doktor</option><option value="dietitian">Diyetisyen</option></select></div>
            <div class="form-group"><label for="login_username">Kullanıcı Adı:</label><input type="text" id="login_username" name="username" required></div>
            <div class="form-group"><label for="login_password">Şifre:</label><input type="password" id="login_password" name="password" required></div>
            <input type="submit" value="Giriş Yap">
        </form>
    </div>

    <div id="register-form" style="display:none;">
        <h2>📝 Kayıt Ol</h2>
        <form method="POST" action="/register">
            <div class="form-group"><label for="reg_role">Rol:</label><select id="reg_role" name="role" onchange="toggleFields(this.value)"><option value="patient">Hasta</option><option value="doctor">Doktor</option><option value="dietitian">Diyetisyen</option></select></div>
            
            <div class="form-group"><label for="reg_username">Kullanıcı Adı:</label><input type="text" id="reg_username" name="username" required></div>
            <div class="form-group"><label for="reg_password">Şifre:</label><input type="password" id="reg_password" name="password" required></div>
            <div class="form-group"><label for="reg_password_confirm">Şifre Onayı:</label><input type="password" id="reg_password_confirm" name="password_confirm" required></div>
            <div class="form-group"><label for="reg_email">E-posta:</label><input type="email" id="reg_email" name="email" required></div>
            <div class="form-group"><label for="reg_tc_kimlik">TC Kimlik No:</label><input type="text" id="reg_tc_kimlik" name="tc_kimlik" required></div>
            <div class="form-group"><label for="reg_birth_date">Doğum Tarihi:</label><input type="date" id="reg_birth_date" name="birth_date" required></div>
            <div class="form-group"><label for="reg_gender">Cinsiyet:</label><select id="reg_gender" name="gender"><option value="Erkek">Erkek</option><option value="Kadın">Kadın</option><option value="Diğer">Diğer</option></select></div>

            <div id="clinician-fields" style="border-left: 3px solid #ffc107; padding-left: 10px; display:none;">
                <h3 style="color: #ffc107;">Klinik Bilgileri</h3>
                <div class="form-group"><label for="reg_hospital">Hastane/Kurum:</label><input type="text" id="reg_hospital" name="hospital"></div>
                <div class="form-group"><label for="reg_phone">Telefon No:</label><input type="text" id="reg_phone" name="phone"></div>
            </div>

            <div id="patient-fields" style="border-left: 3px solid #007bff; padding-left: 10px; display:block;">
                <h3 style="color: #007bff;">Klinik Seçimi (Seçmek zorunlu değildir)</h3>
                <div class="form-group"><label for="doctor_id">Seçeceğiniz Doktor:</label><select id="doctor_id" name="selected_doctor_id"><option value="">-- Seçim Yapın --</option></select></div>
                <div class="form-group"><label for="dietitian_id">Seçeceğiniz Diyetisyen:</label><select id="dietitian_id" name="selected_dietitian_id"><option value="">-- Seçim Yapın --</option></select></div>
                
                <h3 style="color: #007bff;">Diğer Bilgiler (İsteğe Bağlı)</h3>
                <div class="form-group"><label for="reg_height">Boy (cm):</label><input type="text" id="reg_height" name="height"></div>
                <div class="form-group"><label for="reg_weight">Kilo (kg):</label><input type="text" id="reg_weight" name="weight"></div>
            </div>
            
            <input type="submit" value="Kayıt Ol">
        </form>
    </div>
    
</div>
<script>
    // Dinamik alanları göster/gizle
    function toggleFields(role) {
        document.getElementById('patient-fields').style.display = (role === 'patient') ? 'block' : 'none';
        document.getElementById('clinician-fields').style.display = (role !== 'patient') ? 'block' : 'none';
    }

    // Doktor ve Diyetisyenleri API'den çekip select elementlerini doldur
    function loadClinicians() {
        // DÜZELTME: API çağrısı, tarayıcının erişebileceği adrese (localhost:5000) yönlendirildi.
        fetch('http://localhost:5000/api/clinicians') 
            .then(response => {
                if (!response.ok) {
                    // API yanıtı 200 OK değilse hata fırlat
                    throw new Error(`API yanıtı hatalı: ${response.status} (${response.statusText})`);
                }
                return response.json();
            })
            .then(data => {
                const doctorSelect = document.getElementById('doctor_id');
                const dietitianSelect = document.getElementById('dietitian_id');
                
                // Doktorları doldur
                data.doctors.forEach(doc => {
                    const option = document.createElement('option');
                    option.value = doc.id;
                    option.textContent = `${doc.username} (ID: ${doc.id})`;
                    doctorSelect.appendChild(option);
                });

                // Diyetisyenleri doldur
                data.dietitians.forEach(diet => {
                    const option = document.createElement('option');
                    option.value = diet.id;
                    option.textContent = `${diet.username} (ID: ${diet.id})`;
                    dietitianSelect.appendChild(option);
                });
                
                console.log('Klinisyen listesi başarıyla yüklendi.');

            })
            .catch(error => {
                 console.error('Klinisyen listesi yüklenemedi:', error);
                 // Kritik hata mesajını kullanıcıya göster
                 const patientFieldsDiv = document.getElementById('patient-fields');
                 if (patientFieldsDiv) {
                    // Klinisyen listesi başlığını bul ve uyarı ekle
                    const h3 = patientFieldsDiv.querySelector('h3');
                    if (h3) {
                         h3.innerHTML += `<br><span style="color: red; font-size: small;">(Hata: Klinisyen listesi yüklenemedi. Lütfen API'nin (localhost:5000) çalıştığından emin olun.)</span>`;
                    }
                 }
            });
    }

    // Sayfa yüklendiğinde çalıştır
    window.onload = function() {
        toggleFields(document.getElementById('reg_role').value);
        loadClinicians();
    };
</script>
"""

@app.route('/')
def index():
    message = request.args.get('message')
    error = request.args.get('error')
    alert = request.args.get('alert')
    return render_template_string(HTML_TEMPLATE_MAIN, message=message, error=error, alert=alert, API_BASE_URL=API_BASE_URL)

# --- KAYIT ROTASI ---
@app.route('/register', methods=['POST'])
def register_user():
    data = request.form
    role = data['role']
    
    # Şifre kontrolü
    if data['password'] != data['password_confirm']:
        return redirect(url_for('index', alert="Şifreler uyuşmuyor!"))

    # API'ye gönderilecek veriyi oluştur
    new_user_data = {
        "username": data['username'],
        "password": data['password'],
        "email": data['email'],
        "tc_kimlik": data['tc_kimlik'],
        "birth_date": data['birth_date'],
        "gender": data['gender']
    }

    # Role göre özel alanları ekle
    if role == 'patient':
        new_user_data["height"] = data.get('height')
        new_user_data["weight"] = data.get('weight')
        
        # Seçili klinisyenler (boş değilse ekle)
        selected_doctor_id = data.get('selected_doctor_id')
        if selected_doctor_id and selected_doctor_id != "":
            new_user_data["selected_doctor_id"] = selected_doctor_id

        selected_dietitian_id = data.get('selected_dietitian_id')
        if selected_dietitian_id and selected_dietitian_id != "":
            new_user_data["selected_dietitian_id"] = selected_dietitian_id
            
    else:
        new_user_data["hospital"] = data.get('hospital')
        new_user_data["phone"] = data.get('phone')


    endpoint_map = {
        "patient": "/api/patient",
        "doctor": "/api/doctor",
        "dietitian": "/api/dietitian"
    }
    endpoint = endpoint_map.get(role)

    if not endpoint:
        return redirect(url_for('index', error="Geçersiz kullanıcı rolü belirtildi."))
    
    try:
        # Kullanıcıyı Kaydet
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=new_user_data)
        response.raise_for_status()
        
        message = f"**{role.upper()}** {data['username']} başarıyla kaydedildi! Lütfen giriş yapın."
        return redirect(url_for('index', message=message))

    except requests.exceptions.RequestException as e:
        error_msg = f"Kayıt hatası: {e}"
        if e.response is not None:
             error_msg = f"Kayıt hatası: {e.response.json().get('msg', 'Bilinmeyen Hata')}"
        return redirect(url_for('index', error=error_msg))


# --- GİRİŞ ROTASI ---
@app.route('/login', methods=['POST'])
def login_user():
    data = request.form
    username = data['username']
    password = data['password']
    role = data['role']
    
    login_data = {'username': username, 'password': password, 'role': role}
    
    try:
        response = requests.post(f"{API_BASE_URL}/api/login", json=login_data)
        response.raise_for_status()
        
        user_info = response.json()
        user_id = user_info['user_id']
        
        # Başarılı girişten sonra ilgili panele yönlendirme (ID'yi URL'ye ekleyerek)
        if role == 'doctor':
            return redirect(f"http://localhost:5002/?id={user_id}") 
        elif role == 'dietitian':
            return redirect(f"http://localhost:5003/?id={user_id}")
        elif role == 'patient':
            return redirect(f"http://localhost:5004/?id={user_id}")
        else:
             return redirect(url_for('index', message=f"Giriş başarılı, ancak {role} için panel yok. ID: {user_id}"))

    except requests.exceptions.RequestException as e:
        error_msg = f"Giriş hatası: {e}"
        if e.response is not None:
             error_msg = f"Giriş hatası: {e.response.json().get('msg', 'Bilinmeyen Hata')}"
        return redirect(url_for('index', error=error_msg))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)