# patient_client.py (GÜNCELLENDİ - Daha Okunur Görüntüleme)

from flask import Flask, render_template_string, request, jsonify
import requests

# Ana API'mizin çalıştığı adres
API_BASE_URL = "http://saglik_takip_app:5000"

app = Flask(__name__)

# Basit HTML Şablonu (ID'yi dinamik gösterecek şekilde güncellendi)
HTML_TEMPLATE_PATIENT = """
<!doctype html>
<title>Hasta Paneli - ID: {{ patient_id }}</title>
<h1>🩺 Hasta Paneli (ID: {{ patient_id }})</h1>

{% if error %}
    <p style="color: red;">Hata: {{ error }}</p>
{% endif %}

<hr>
<h2>💊 İlaç Çizelgesi (Doktor Tarafından Hazırlanan)</h2>
{% if med_schedules %}
    <table border="1" style="width: 100%; border-collapse: collapse;">
        <tr>
            <th style="padding: 8px; background-color: #f2f2f2;">Gün</th>
            <th style="padding: 8px; background-color: #f2f2f2;">İlaç Adı</th>
            <th style="padding: 8px; background-color: #f2f2f2;">Dozaj</th>
            <th style="padding: 8px; background-color: #f2f2f2;">Kullanım Sıklığı</th>
        </tr>
    {% for schedule in med_schedules %}
        <tr>
            <td style="padding: 8px; text-align: center;">**{{ schedule.day }}**</td>
            <td style="padding: 8px;">{{ schedule.medication_name }}</td>
            <td style="padding: 8px; text-align: center;">{{ schedule.dosage }}</td>
            <td style="padding: 8px; text-align: center;">{{ schedule.frequency }}</td>
        </tr>
    {% endfor %}
    </table>
{% else %}
    <p>Aktif bir ilaç çizelgeniz bulunmamaktadır.</p>
{% endif %}

<hr>
<h2>🍽️ Yemek Çizelgesi (Diyetisyen Tarafından Hazırlanan)</h2>
{% if meal_schedules %}
    <table border="1" style="width: 100%; border-collapse: collapse;">
        <tr>
            <th style="padding: 8px; background-color: #f2f2f2;">Gün</th>
            <th style="padding: 8px; background-color: #f2f2f2;">Öğün</th>
            <th style="padding: 8px; background-color: #f2f2f2;">Porsiyon/İçerik</th>
        </tr>
    {% for schedule in meal_schedules %}
        <tr>
            <td style="padding: 8px; text-align: center;">**{{ schedule.day }}**</td>
            <td style="padding: 8px; text-align: center;">{{ schedule.meal_name }}</td>
            <td style="padding: 8px;">{{ schedule.portion }}</td>
        </tr>
    {% endfor %}
    </table>
{% else %}
    <p>Aktif bir yemek çizelgeniz bulunmamaktadır.</p>
{% endif %}

<hr>
<p>Verileriniz, Sağlık Takip API'sinden çekilmektedir.</p>
"""

@app.route('/')
def index():
    """API'den hastanın ilaç ve yemek çizelgelerini çeker ve görüntüler."""
    # ID'yi URL sorgu parametresinden al
    patient_id = request.args.get('id', 1, type=int) # Varsayılan olarak 1 kullan
    if patient_id is None:
        return render_template_string(HTML_TEMPLATE_PATIENT, patient_id="Bilinmiyor", error="Giriş ID'si eksik.")
        
    med_schedules = []
    meal_schedules = []
    error = None
    
    try:
        # 1. İlaç Çizelgesini Çekme (Dinamik ID)
        med_response = requests.get(f"{API_BASE_URL}/api/patient/{patient_id}/schedule/medication")
        med_response.raise_for_status()
        # İlaç çizelgesi verisi, istemcide kullanılmak üzere dönüştürülür
        med_schedules = med_response.json()

        # 2. Yemek Çizelgesini Çekme (Dinamik ID)
        meal_response = requests.get(f"{API_BASE_URL}/api/patient/{patient_id}/schedule/meal")
        meal_response.raise_for_status()
        # Yemek çizelgesi verisi, istemcide kullanılmak üzere dönüştürülür
        meal_schedules = meal_response.json()
        
    except requests.exceptions.RequestException as e:
        error = f"API'ye ulaşım hatası: {e}"
        print(error)

    return render_template_string(
        HTML_TEMPLATE_PATIENT, 
        patient_id=patient_id, 
        med_schedules=med_schedules, 
        meal_schedules=meal_schedules,
        error=error
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)