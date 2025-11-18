# doctor_client.py (SON ÇÖZÜM: Onaylanan hastayı Pending listesinden alıp Approved listesine ekler)

from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import requests 
import json 
import re 

# Ana API'mizin çalıştığı adres
API_BASE_URL = "http://saglik_takip_app:5000"

app = Flask(__name__)

# Basit HTML Şablonu (Önceki dinamik versiyona geri döndü)
HTML_TEMPLATE = """
<!doctype html>
<title>Doktor Paneli - ID: {{ doctor_id }}</title>
<h1>👨‍⚕️ Doktor Paneli (ID: {{ doctor_id }})</h1>

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
            <form method="POST" action="/approve_patient/{{ patient.id }}?id={{ doctor_id }}" style="display:inline; margin-left: 10px;">
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

<h2>2. Onaylanmış Hastalar ve İlaç Çizelgesi İşlemleri</h2>

{% if approved_patients %}
    <p>İlaç çizelgesi oluşturmak/güncellemek için aşağıdaki hastanın işlemlerini kullanın.</p>
    <ul>
    {% for patient in approved_patients %}
        <li style="margin-bottom: 10px;">
            ID: {{ patient.id }}, Ad: **{{ patient.username }}**
            <button onclick="document.getElementById('schedule_form_{{ patient.id }}').style.display='block'" style="margin-left: 10px;">💊 İlaç Çizelgesi Oluştur/Güncelle</button>
            <a href="/view_medication/{{ patient.id }}?id={{ doctor_id }}" target="_blank" style="margin-left: 10px; text-decoration: none;">📄 Çizelgeyi Görüntüle</a>
        </li>
        
        <div id="schedule_form_{{ patient.id }}" style="display:none; margin-left: 20px; border: 1px solid #007bff; padding: 15px; margin-bottom: 20px; border-radius: 5px;">
            <h3>Hasta ID {{ patient.id }} için İlaç Çizelgesi (JSON Formatı)</h3>
            <form method="POST" action="/create_schedule/{{ patient.id }}?id={{ doctor_id }}">
                <p>Yeni bir ilaç programı girmek için JSON kullanın (Mevcut olan silinir):</p>
                <p style="font-size: small; color: gray;">*Alanlar: "day", "medication", "dosage", "frequency"</p>
                <textarea name="schedule_data" rows="8" cols="70" required>[
  {"day": "Pazartesi", "medication": "Yeni İlaç 1", "dosage": "500 mg", "frequency": "Günde 1"},
  {"day": "Salı", "medication": "Yeni İlaç 2", "dosage": "10 mg", "frequency": "Günde 2"}
]</textarea><br>
                <input type="submit" value="İlaç Çizelgesini Gönder">
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
    doctor_id = request.args.get('id', 2, type=int) 
    if doctor_id is None:
        return render_template_string(HTML_TEMPLATE, doctor_id="Bilinmiyor", error="Giriş ID'si eksik.")

    pending_patients = []
    approved_patients = []
    message = request.args.get('message')
    error = request.args.get('error')
    
    try:
        # Onay bekleyen hastaları çek
        pending_response = requests.get(f"{API_BASE_URL}/api/doctor/{doctor_id}/patients/pending")
        pending_response.raise_for_status()
        pending_patients = pending_response.json()
        
        # ONAY KRİTİK NOKTASI: Onaylandıktan sonra URL'den gelen mesajı kontrol et
        if message and "başarıyla onaylandı" in message:
            match = re.search(r"Hasta ID (\d+) başarıyla onaylandı!", message)
            if match:
                patient_id = int(match.group(1))
                
                # Geçici olarak onaylanan hastayı pending listesinden bulmaya çalış
                # (Pending listesi API çağrısından sonra güncellenir, bu nedenle burada bulamayız.)
                # Bunun yerine, onaylanan hastayı doğrudan Approved listesine ekliyoruz.
                
                # Doğru kullanıcı adını bulmak için tüm kullanıcıları çekemediğimiz için,
                # sadece ID ve genel bir isimle ekliyoruz.
                approved_patients.append({
                    "id": patient_id, 
                    "username": f"Hasta ID {patient_id} (Yeni Onaylanan)"
                })
        
        # NOT: Eğer Ahmet (ID: 1), Doctor Zeynep (ID: 2) tarafından onaylanmışsa, 
        # onu da manuel olarak approved listesine ekleyebiliriz (Test için). 
        # Ancak bunu yapmazsak, sadece yeni onaylanan hastalar görünür.
        # Bu sorunun kök nedeni, API'de '/approved' rotasının olmamasıdır.
        # Basitlik için sadece yeni onaylananı gösteriyoruz.

    except requests.exceptions.RequestException as e:
        error = f"API Hatası: {e}"

    return render_template_string(
        HTML_TEMPLATE, 
        doctor_id=doctor_id, 
        pending_patients=pending_patients, 
        approved_patients=approved_patients, # Yeni: Dinamik liste
        message=message,
        error=error
    )

# --- 2. Hastayı Onaylama ---
@app.route('/approve_patient/<int:patient_id>', methods=['POST'])
def approve_patient(patient_id):
    doctor_id = request.args.get('id', type=int)
    if not doctor_id:
        return redirect(url_for('index', error="Doktor ID eksik."))
        
    try:
        response = requests.post(f"{API_BASE_URL}/api/doctor/{doctor_id}/patients/approve/{patient_id}")
        response.raise_for_status()
        
        # Onaylandıktan sonra index'e yönlendir ve mesaj göster
        return redirect(url_for('index', id=doctor_id, message=f"Hasta ID {patient_id} başarıyla onaylandı! Artık ilaç çizelgesi oluşturabilirsiniz."))

    except requests.exceptions.RequestException as e:
        error_msg = f"Onay hatası: {e}"
        if e.response is not None:
             try:
                 error_msg = f"Onay hatası: {e.response.json().get('msg', 'Bilinmeyen Hata')}"
             except:
                 pass
        return redirect(url_for('index', id=doctor_id, error=error_msg))

# --- 3. İlaç Çizelgesi Oluşturma ---
@app.route('/create_schedule/<int:patient_id>', methods=['POST'])
def create_schedule(patient_id):
    # Bu rota, HTML formundan gelen doğru hasta ID'sini alacaktır (Meryem'in ID'si).
    doctor_id = request.args.get('id', type=int)
    if not doctor_id:
        return redirect(url_for('index', error="Doktor ID eksik."))
        
    try:
        schedule_data_str = request.form['schedule_data']
        schedule_data = json.loads(schedule_data_str)
        
        # API rotasını dinamik ID ile çağır
        endpoint = f"{API_BASE_URL}/api/doctor/{doctor_id}/patient/{patient_id}/schedule/medication"
        response = requests.post(endpoint, json=schedule_data)
        response.raise_for_status()
        
        return redirect(url_for('index', id=doctor_id, message=f"Hasta {patient_id} için ilaç çizelgesi oluşturuldu!"))

    except json.JSONDecodeError:
        return redirect(url_for('index', id=doctor_id, error="Geçersiz JSON formatı girdiniz."))
    except requests.exceptions.RequestException as e:
        error_msg = f"Çizelge oluşturma hatası: {e}"
        if e.response is not None:
             try:
                 error_msg = f"Çizelge oluşturma hatası: {e.response.json().get('msg', 'Bilinmeyen Hata')}"
             except:
                 pass
        return redirect(url_for('index', id=doctor_id, error=error_msg))
        
# --- 4. İlaç Çizelgesini Görüntüleme (Hasta Rotası Üzerinden) ---
@app.route('/view_medication/<int:patient_id>')
def view_medication(patient_id):
    try:
        # Hastanın kendi görme rotasını çağırır
        endpoint = f"{API_BASE_URL}/api/patient/{patient_id}/schedule/medication"
        response = requests.get(endpoint)
        response.raise_for_status()
        
        return f"<pre>{json.dumps(response.json(), indent=4, ensure_ascii=False)}</pre>", 200
    
    except requests.exceptions.RequestException as e:
        return jsonify(error=f"İlaç çizelgesi görüntüleme hatası: {e}"), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)