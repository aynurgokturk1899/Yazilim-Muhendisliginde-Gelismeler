# client_app.py

from flask import Flask, jsonify, render_template_string, request, redirect, url_for
import requests

# Ana API'mizin çalıştığı adres
API_BASE_URL = "http://saglik_takip_app:5000"
# Eğer Docker kullanmıyorsanız ve doğrudan yerel makinenizde çalıştırıyorsanız,
# bu adresi "http://127.0.0.1:5000" olarak değiştirmelisiniz.

app = Flask(__name__)

# Basit bir HTML şablonu (Bu kısım aynı kalmıştır)
HTML_TEMPLATE = """
<!doctype html>
<title>Sağlık Takip İstemcisi</title>
<h1>API İstemci Uygulaması</h1>
<h2>Kullanıcılar</h2>
<ul>
{% for user in users %}
    <li>ID: {{ user.id }}, Ad: {{ user.name }}, Rol: {{ user.role }}</li>
{% endfor %}
</ul>

<hr>

<h2>Yeni Kullanıcı Ekle</h2>
<form method="POST" action="/add_user">
    <label for="id">ID:</label>
    <input type="text" id="id" name="id" required><br><br>
    <label for="name">Ad:</label>
    <input type="text" id="name" name="name" required><br><br>
    <label for="role">Rol:</label>
    <select id="role" name="role">
        <option value="patient">Hasta</option>
        <option value="doctor">Doktor</option>
        <option value="dietitian">Diyetisyen</option>
    </select><br><br>
    <input type="submit" value="Ekle">
</form>

{% if message %}
    <p style="color: green;">{{ message }}</p>
{% endif %}
"""

@app.route('/')
def index():
    """Ana API'den kullanıcı listesini çeker ve görüntüler."""
    users = []
    message = request.args.get('message') # URL'den mesajı al
    try:
        # API'deki /api/users endpoint'ine GET isteği gönder
        response = requests.get(f"{API_BASE_URL}/api/users")
        response.raise_for_status()
        users = response.json()
    except requests.exceptions.RequestException as e:
        # API'ye ulaşılamazsa veya hata dönerse mesajı hazırla
        api_error_message = f"API'ye ulaşılamadı veya bir hata oluştu: {e}"
        print(api_error_message)
        # Eğer bir ekleme mesajı yoksa API hatasını göster
        if not message:
             message = api_error_message

    return render_template_string(HTML_TEMPLATE, users=users, message=message)

@app.route('/add_user', methods=['POST'])
def add_user():
    """Ana API'ye yeni kullanıcı eklemek için POST isteği gönderir. (Düzeltildi)"""
    data = request.form
    new_user = {
        # memory_db ID'leri int beklediği için cast ediyoruz.
        "id": int(data['id']), 
        "name": data['name'],
        "role": data['role']
    }

    # HATA DÜZELTMESİ: API'deki rotalar tekildir (/api/doctor, /api/patient).
    # Rol adının sonuna 's' ekleyen önceki mantık yerine doğru endpoint'leri eşleştiriyoruz.
    endpoint_map = {
        "patient": "/api/patient",
        "doctor": "/api/doctor",
        "dietitian": "/api/dietitian"
    }

    # Kullanıcı rolüne göre doğru endpoint'i seç
    endpoint = endpoint_map.get(new_user['role'])
    
    if not endpoint:
        error_message = f"Geçersiz kullanıcı rolü belirtildi: {new_user['role']}"
        return redirect(url_for('index', message=error_message))

    try:
        # Yeni kullanıcı ekleme endpoint'ine POST isteği gönder
        response = requests.post(f"{API_BASE_URL}{endpoint}", json=new_user)
        response.raise_for_status()

        return redirect(url_for('index', message="Kullanıcı başarıyla eklendi!"))

    except requests.exceptions.RequestException as e:
        error_message = f"Kullanıcı eklenirken hata: {e}"
        print(error_message)
        # Hata mesajını URL'ye ekleyerek index'e geri dön
        return redirect(url_for('index', message=error_message))

if __name__ == '__main__':
    # Bu istemci uygulamasını 5001 portunda çalıştıracağız
    app.run(host='0.0.0.0', port=5001, debug=True)