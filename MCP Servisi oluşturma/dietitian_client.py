# dietitian_client.py (SON VE KALICI ÇÖZÜM)

from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import requests
import json 
import re 

# Ana API'mizin çalıştığı adres
API_BASE_URL = "http://saglik_takip_app:5000"

app = Flask(__name__)

# Basit HTML Şablonu (Mevcut HTML)
HTML_TEMPLATE_DIETITIAN = """
<!doctype html>
<title>Diyetisyen Paneli - ID: {{ dietitian_id }}</title>
<h1>🥗 Diyetisyen Paneli (ID: {{ dietitian_id }})</h1>

{% if message %}
    <p style="color: green;">{{ message }}</p>
{% endif %}
{% if error %}
    <p style="color: red;">Hata: {{ error }}</p>
{% endif %}

<hr>

<h2>1. Onay Bekleyen Hastalar</h2>

{% if pending_patients %}
    <ul>
    {% for patient in pending_patients %}
        <li>
            ID: {{ patient.id }}, Ad: **{{ patient.username }}** (E-posta: {{ patient.email }})
            <form method="POST" action="/approve_patient/{{ patient.id }}?id={{ dietitian_id }}" style="display:inline; margin-left: 10px;">
                <button type="submit">✅ Onayla</button>
            </form>
            <span style="font-size: small; color: orange;">(Onay Bekleniyor)</span>
        </li>
    {% endfor %}
    </ul>
{% else %}
    <p>Onay bekleyen hasta bulunmamaktadır.</p>
{% endif %}

<hr>

<h2>2. Onaylanmış Hastalar ve Yemek Çizelgesi İşlemleri</h2>

{% if approved_patients %}
    <p>Yemek çizelgesi oluşturmak/güncellemek için aşağıdaki hastanın işlemlerini kullanın.</p>
    <ul>
    {% for patient in approved_patients %}
        <li style="margin-bottom: 10px;">
            ID: {{ patient.id }}, Ad: **{{ patient.username }}**
            <button onclick="document.getElementById('meal_form_{{ patient.id }}').style.display='block'" style="margin-left: 10px;">🍽️ Yemek Çizelgesi Oluştur/Güncelle</button>
            <a href="/view_meal/{{ patient.id }}?id={{ dietitian_id }}" target="_blank" style="margin-left: 10px; text-decoration: none;">📄 Çizelgeyi Görüntüle</a>
        </li>
        
        <div id="meal_form_{{ patient.id }}" style="display:none; margin-left: 20px; border: 1px solid #28a745; padding: 15px; margin-bottom: 20px; border-radius: 5px;">
            <h3>Hasta ID {{ patient.id }} için Yemek Çizelgesi (JSON Formatı)</h3>
            <form method="POST" action="/create_meal_schedule/{{ patient.id }}?id={{ dietitian_id }}">
                <p>Yeni bir yemek programı girmek için JSON kullanın (Mevcut olan silinir):</p>
                <p style="font-size: small; color: gray;">*Alanlar: "day", "meal", "portion"</p>
                <textarea name="schedule_data" rows="8" cols="70" required>[
  {"day": "Pazartesi", "meal": "Kahvaltı", "portion": "2 yumurta, salatalık"},
  {"day": "Salı", "meal": "Öğle", "portion": "Izgara tavuk, bol salata"}
]</textarea><br>
                <input type="submit" value="Yemek Çizelgesini Gönder">
            </form>
        </div>
    {% endfor %}
    </ul>
{% else %}
    <p>Şu anda yönetilebilecek onaylanmış hastanız bulunmamaktadır. Lütfen listeden bir hastayı onaylayın.</p>
{% endif %}
"""

# --- 1. Onay Bekleyen ve Onaylanmış Hastaları Görüntüleme ---
@app.route('/')
def index():
    dietitian_id = request.args.get('id', 3, type=int) 
    if dietitian_id is None:
        return render_template_string(HTML_TEMPLATE_DIETITIAN, dietitian_id="Bilinmiyor", error="Giriş ID'si eksik.")

    pending_patients = []
    approved_patients = []
    message = request.args.get('message')
    error = request.args.get('error')
    
    try:
        # Onay bekleyen hastaları çek
        pending_response = requests.get(f"{API_BASE_URL}/api/dietitian/{dietitian_id}/patients/pending")
        pending_response.raise_for_status()
        pending_patients = pending_response.json()
        
        # YENİ EKLEME: Onaylanmış hastaları çek (Kalıcı Çözüm)
        approved_response = requests.get(f"{API_BASE_URL}/api/dietitian/{dietitian_id}/patients/approved")
        approved_response.raise_for_status()
        approved_patients = approved_response.json()
        
        # NOT: Geçici ekleme ve manuel test mantığı, API'den kalıcı liste çekildiği için artık gerekli değildir ve kaldırılmıştır.

    except requests.exceptions.RequestException as e:
        error = f"API Hatası: {e}"
        if hasattr(e, 'response') and e.response is not None:
             error = f"API Hatası: {e.response.status_code} - {e.response.text}"

    return render_template_string(
        HTML_TEMPLATE_DIETITIAN, 
        dietitian_id=dietitian_id, 
        pending_patients=pending_patients, 
        approved_patients=approved_patients, # Artık API'den gelen kalıcı liste
        message=message,
        error=error
    )

# --- 2. Hastayı Onaylama ---
@app.route('/approve_patient/<int:patient_id>', methods=['POST'])
def approve_patient_route(patient_id):
    dietitian_id = request.args.get('id', type=int)
    if not dietitian_id:
        return redirect(url_for('index', error="Diyetisyen ID eksik."))
        
    try:
        response = requests.post(f"{API_BASE_URL}/api/dietitian/{dietitian_id}/patients/approve/{patient_id}")
        response.raise_for_status()
        
        # Onaylandıktan sonra index'e yönlendir ve mesaj göster
        return redirect(url_for('index', id=dietitian_id, message=f"Hasta ID {patient_id} başarıyla onaylandı! Artık yemek çizelgesi oluşturabilirsiniz."))

    except requests.exceptions.RequestException as e:
        error_msg = f"Onay hatası: {e}"
        if e.response is not None:
             try:
                 error_msg = f"Onay hatası: {e.response.json().get('msg', 'Bilinmeyen Hata')}"
             except:
                 pass
        return redirect(url_for('index', id=dietitian_id, error=error_msg))

# --- 3. Yemek Çizelgesi Oluşturma (Dinamik ID'yi kullanır) ---
@app.route('/create_meal_schedule/<int:patient_id>', methods=['POST'])
def create_meal_schedule(patient_id):
    dietitian_id = request.args.get('id', type=int)
    if not dietitian_id:
        return redirect(url_for('index', error="Diyetisyen ID eksik."))
        
    try:
        schedule_data_str = request.form['schedule_data']
        schedule_data = json.loads(schedule_data_str) 
        
        # API rotasını dinamik ID ile çağır
        endpoint = f"{API_BASE_URL}/api/dietitian/{dietitian_id}/patient/{patient_id}/schedule/meal"
        response = requests.post(endpoint, json=schedule_data)
        response.raise_for_status()
        
        return redirect(url_for('index', id=dietitian_id, message=f"Hasta {patient_id} için yemek çizelgesi oluşturuldu!"))

    except json.JSONDecodeError:
        return redirect(url_for('index', id=dietitian_id, error="Geçersiz JSON formatı girdiniz."))
    except requests.exceptions.RequestException as e:
        error_msg = f"Çizelge oluşturma hatası: {e}"
        if e.response is not None:
             try:
                 error_msg = f"Çizelge oluşturma hatası: {e.response.json().get('msg', 'Bilinmeyen Hata')}"
             except:
                 pass
        return redirect(url_for('index', id=dietitian_id, error=error_msg))
        
# --- 4. Yemek Çizelgesini Görüntüleme ---\
@app.route('/view_meal/<int:patient_id>')
def view_meal(patient_id):
    try:
        # Hasta rotasını çağır
        endpoint = f"{API_BASE_URL}/api/patient/{patient_id}/schedule/meal"
        response = requests.get(endpoint)
        response.raise_for_status()
        
        # JSON çıktısını düzenli formatta göster
        return f"<pre>{json.dumps(response.json(), indent=4, ensure_ascii=False)}</pre>", 200
    
    except requests.exceptions.RequestException as e:
        return jsonify(error=f"Yemek çizelgesi görüntüleme hatası: {e}"), 500

# --- 5. İlaç Çizelgesini Görüntüleme (Sadece yetki kontrolü için) ---
@app.route('/view_medication/<int:patient_id>')
def view_medication(patient_id):
    dietitian_id = request.args.get('id', type=int)
    if not dietitian_id:
        return jsonify(error="Diyetisyen ID eksik."), 400
        
    try:
        # API rotasını dinamik ID ile çağır (Erişim kontrolü için)
        endpoint = f"{API_BASE_URL}/api/dietitian/{dietitian_id}/patient/{patient_id}/schedule/medication"
        response = requests.get(endpoint)
        response.raise_for_status()
        
        return f"<pre>{json.dumps(response.json(), indent=4, ensure_ascii=False)}</pre>", 200
    except requests.exceptions.RequestException as e:
        return jsonify(error=f"İlaç çizelgesi görüntüleme hatası: {e}"), 500


if __name__ == '__main__':
    # Diyetisyen Paneli genellikle 5003 portunda çalışır
    app.run(host='0.0.0.0', port=5003, debug=True)