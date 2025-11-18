# dietitian_client.py

from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import requests

# Ana API'mizin çalıştığı adres
API_BASE_URL = "http://saglik_takip_app:5000"

# Sabit Diyetisyen ID'si (Örnek: Diyetisyen Can)
DIETITIAN_ID = 3

app = Flask(__name__)

# Basit HTML Şablonu
HTML_TEMPLATE_DIETITIAN = """
<!doctype html>
<title>Diyetisyen Paneli - ID: {{ dietitian_id }}</title>
<h1>🥗 Diyetisyen Paneli</h1>
<h2>Onay Bekleyen Hastalar</h2>

{% if message %}
    <p style="color: green;">{{ message }}</p>
{% endif %}
{% if error %}
    <p style="color: red;">Hata: {{ error }}</p>
{% endif %}

{% if pending_patients %}
    <ul>
    {% for patient in pending_patients %}
        <li>
            ID: {{ patient.id }}, Ad: {{ patient.username }} (Rol: {{ patient.role }})
            <form method="POST" action="/approve_patient/{{ patient.id }}" style="display:inline;">
                <button type="submit">Onayla</button>
            </form>
            <button onclick="document.getElementById('meal_form_{{ patient.id }}').style.display='block'">Yemek Çizelgesi Oluştur</button>
        </li>
        
        <div id="meal_form_{{ patient.id }}" style="display:none; margin-left: 20px; border: 1px solid #ccc; padding: 10px; margin-bottom: 15px;">
            <h3>Hasta {{ patient.id }} için Yemek Çizelgesi</h3>
            <form method="POST" action="/create_meal_schedule/{{ patient.id }}">
                <p>Yeni bir yemek programı girmek için JSON kullanın (Mevcut olan silinir):</p>
                <textarea name="schedule_data" rows="8" cols="50" required>[
  {"day": "Pazartesi", "meal": "Kahvaltı", "portion": "2 yumurta, salatalık"},
  {"day": "Salı", "meal": "Öğle", "portion": "Izgara tavuk, bol salata"}
]</textarea><br>
                <input type="submit" value="Yemek Çizelgesini Gönder">
            </form>
        </div>
    {% endfor %}
    </ul>
{% else %}
    <p>Onay bekleyen hasta bulunmamaktadır.</p>
{% endif %}

<hr>

<h2>Hasta Ahmet (ID: 1) Çizelgeleri (Onaylandıysa Görünür)</h2>
<a href="/view_meal/1">Yemek Çizelgesini Görüntüle</a><br>
<a href="/view_medication/1">İlaç Çizelgesini Görüntüle</a>
"""

# --- 1. Onay Bekleyen Hastaları Görüntüleme ---
@app.route('/')
def index():
    """Diyetisyenden onay bekleyen hastaları API'den çeker."""
    pending_patients = []
    message = request.args.get('message')
    error = request.args.get('error')
    
    try:
        # GET /api/dietitian/3/patients/pending rotasını çağır
        response = requests.get(f"{API_BASE_URL}/api/dietitian/{DIETITIAN_ID}/patients/pending")
        response.raise_for_status()
        pending_patients = response.json()
        
    except requests.exceptions.RequestException as e:
        error = f"API Hatası: {e}"
        print(error)

    return render_template_string(
        HTML_TEMPLATE_DIETITIAN, 
        dietitian_id=DIETITIAN_ID, 
        pending_patients=pending_patients, 
        message=message,
        error=error
    )

# --- 2. Hastayı Onaylama ---
@app.route('/approve_patient/<int:patient_id>', methods=['POST'])
def approve_patient(patient_id):
    """Hastaya erişim iznini onaylar."""
    try:
        # POST /api/dietitian/3/patients/approve/1 rotasını çağır
        response = requests.post(f"{API_BASE_URL}/api/dietitian/{DIETITIAN_ID}/patients/approve/{patient_id}")
        response.raise_for_status()
        
        return redirect(url_for('index', message="Hasta başarıyla onaylandı!"))

    except requests.exceptions.RequestException as e:
        return redirect(url_for('index', error=f"Onay hatası: {e}"))

# --- 3. Yemek Çizelgesi Oluşturma ---
@app.route('/create_meal_schedule/<int:patient_id>', methods=['POST'])
def create_meal_schedule(patient_id):
    """Hastaya yeni bir yemek çizelgesi atar."""
    try:
        schedule_data_str = request.form['schedule_data']
        
        # JSON verisini Python listesine dönüştür
        import json
        schedule_data = json.loads(schedule_data_str)
        
        # POST /api/dietitian/3/patient/1/schedule/meal rotasını çağır
        endpoint = f"{API_BASE_URL}/api/dietitian/{DIETITIAN_ID}/patient/{patient_id}/schedule/meal"
        response = requests.post(endpoint, json=schedule_data)
        response.raise_for_status()
        
        return redirect(url_for('index', message=f"Hasta {patient_id} için yemek çizelgesi oluşturuldu!"))

    except json.JSONDecodeError:
        return redirect(url_for('index', error="Geçersiz JSON formatı girdiniz."))
    except requests.exceptions.RequestException as e:
        return redirect(url_for('index', error=f"Çizelge oluşturma hatası: {e}"))

# --- 4. Yemek Çizelgesini Görüntüleme ---
@app.route('/view_meal/<int:patient_id>')
def view_meal(patient_id):
    """Hastanın yemek çizelgesini görüntüler."""
    try:
        # GET /api/patient/1/schedule/meal rotasını çağırır
        endpoint = f"{API_BASE_URL}/api/patient/{patient_id}/schedule/meal"
        response = requests.get(endpoint)
        response.raise_for_status()
        
        schedules = response.json()
        
        return jsonify(schedules) # Basitçe JSON olarak döndürüyoruz
    
    except requests.exceptions.RequestException as e:
        return jsonify(error=f"Yemek çizelgesi görüntüleme hatası: {e}"), 500

# --- 5. İlaç Çizelgesini Görüntüleme ---
@app.route('/view_medication/<int:patient_id>')
def view_medication(patient_id):
    """Hastanın ilaç çizelgesini görüntüler (Sadece görme yetkisi)."""
    try:
        # GET /api/dietitian/3/patient/1/schedule/medication rotasını çağırır
        endpoint = f"{API_BASE_URL}/api/dietitian/{DIETITIAN_ID}/patient/{patient_id}/schedule/medication"
        response = requests.get(endpoint)
        response.raise_for_status()
        
        schedules = response.json()
        
        return jsonify(schedules) # Basitçe JSON olarak döndürüyoruz
    
    except requests.exceptions.RequestException as e:
        return jsonify(error=f"İlaç çizelgesi görüntüleme hatası: {e}"), 500


if __name__ == '__main__':
    # Bu yeni istemci uygulamasını 5003 portunda çalıştıracağız
    app.run(host='0.0.0.0', port=5003, debug=True)