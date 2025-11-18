# patient_client.py

from flask import Flask, render_template_string, request, jsonify
import requests

# Ana API'mizin çalıştığı adres
API_BASE_URL = "http://saglik_takip_app:5000"

# Sabit Hasta ID'si (Örnek: Hasta Ahmet)
PATIENT_ID = 1

app = Flask(__name__)

# Basit HTML Şablonu
HTML_TEMPLATE_PATIENT = """
<!doctype html>
<title>Hasta Paneli - ID: {{ patient_id }}</title>
<h1>🩺 Hasta Ahmet'in Paneli</h1>

{% if error %}
    <p style="color: red;">Hata: {{ error }}</p>
{% endif %}

<hr>
<h2>💊 İlaç Çizelgesi (Doktor Tarafından Hazırlanan)</h2>
{% if med_schedules %}
    <ul>
    {% for schedule in med_schedules %}
        <li>
            **{{ schedule.day }}**: {{ schedule.medication_name }} (Dozaj: {{ schedule.dosage }}, Sıklık: {{ schedule.frequency }})
        </li>
    {% endfor %}
    </ul>
{% else %}
    <p>Aktif bir ilaç çizelgeniz bulunmamaktadır.</p>
{% endif %}

<hr>
<h2>🍽️ Yemek Çizelgesi (Diyetisyen Tarafından Hazırlanan)</h2>
{% if meal_schedules %}
    <ul>
    {% for schedule in meal_schedules %}
        <li>
            **{{ schedule.day }} / {{ schedule.meal_name }}**: {{ schedule.portion }}
        </li>
    {% endfor %}
    </ul>
{% else %}
    <p>Aktif bir yemek çizelgeniz bulunmamaktadır.</p>
{% endif %}

<hr>
<p>Verileriniz, Sağlık Takip API'sinden çekilmektedir.</p>
"""

@app.route('/')
def index():
    """API'den hastanın ilaç ve yemek çizelgelerini çeker ve görüntüler."""
    med_schedules = []
    meal_schedules = []
    error = None
    
    try:
        # 1. İlaç Çizelgesini Çekme (GET /api/patient/1/schedule/medication)
        med_response = requests.get(f"{API_BASE_URL}/api/patient/{PATIENT_ID}/schedule/medication")
        med_response.raise_for_status()
        med_schedules = med_response.json()

        # 2. Yemek Çizelgesini Çekme (GET /api/patient/1/schedule/meal)
        meal_response = requests.get(f"{API_BASE_URL}/api/patient/{PATIENT_ID}/schedule/meal")
        meal_response.raise_for_status()
        meal_schedules = meal_response.json()
        
    except requests.exceptions.RequestException as e:
        error = f"API'ye ulaşım hatası: {e}"
        print(error)

    return render_template_string(
        HTML_TEMPLATE_PATIENT, 
        patient_id=PATIENT_ID, 
        med_schedules=med_schedules, 
        meal_schedules=meal_schedules,
        error=error
    )

if __name__ == '__main__':
    # Bu yeni istemci uygulamasını 5004 portunda çalıştıracağız
    app.run(host='0.0.0.0', port=5004, debug=True)