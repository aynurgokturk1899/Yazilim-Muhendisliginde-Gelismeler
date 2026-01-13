# flask_projem/patient_client.py (EN GÜNCEL HALİ)

from flask import Flask, render_template_string, request, jsonify
import requests

API_BASE_URL = "http://saglik_takip_app:5000"
LOGIN_APP_URL = "http://localhost:5001"

app = Flask(__name__)

HTML_TEMPLATE_PATIENT = """
<!doctype html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Hasta Paneli - ID: {{ patient_id }}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; color: #333; margin: 0; padding: 0; }
        .container { max-width: 900px; margin: 40px auto; background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); }
        
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #007bff; padding-bottom: 20px; margin-bottom: 30px; }
        .header h1 { margin: 0; color: #007bff; font-size: 24px; }
        .logout-btn { background-color: #dc3545; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 14px; transition: background 0.3s; }
        .logout-btn:hover { background-color: #c82333; }

        /* Profil Kartı Stili */
        .profile-card { background: #e9ecef; padding: 20px; border-radius: 8px; margin-bottom: 30px; border-left: 5px solid #17a2b8; }
        .profile-title { font-size: 18px; font-weight: bold; margin-bottom: 10px; color: #17a2b8; }
        .profile-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; }
        .profile-item { background: white; padding: 10px; border-radius: 5px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .profile-item strong { display: block; color: #555; font-size: 12px; margin-bottom: 3px; }
        .profile-item span { font-weight: 600; color: #333; }

        h2 { color: #28a745; margin-top: 30px; font-size: 20px; border-left: 5px solid #28a745; padding-left: 10px; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; background-color: white; }
        th, td { padding: 12px 15px; border: 1px solid #ddd; text-align: left; }
        th { background-color: #f8f9fa; font-weight: bold; color: #555; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        
        .empty-msg { color: #777; font-style: italic; background: #f9f9f9; padding: 15px; border-radius: 5px; margin-top: 10px; }
        .error { color: #721c24; background-color: #f8d7da; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>🩺 Hasta Paneli</h1>
        <a href="{{ login_url }}" class="logout-btn">Çıkış Yap</a>
    </div>

    {% if error %} <div class="error">⚠️ {{ error }}</div> {% endif %}

    <div class="profile-card">
        <div class="profile-title">👤 Profil Bilgilerim</div>
        {% if profile %}
        <div class="profile-grid">
            <div class="profile-item"><strong>Ad Soyad</strong> <span>{{ profile.username }}</span></div>
            <div class="profile-item"><strong>E-Posta</strong> <span>{{ profile.email }}</span></div>
            <div class="profile-item"><strong>TC Kimlik</strong> <span>{{ profile.tc_kimlik }}</span></div>
            <div class="profile-item"><strong>Doğum Tarihi</strong> <span>{{ profile.birth_date }}</span></div>
            <div class="profile-item"><strong>Cinsiyet</strong> <span>{{ profile.gender }}</span></div>
            <div class="profile-item"><strong>Boy</strong> <span>{{ profile.height or '-' }} cm</span></div>
            <div class="profile-item"><strong>Kilo</strong> <span>{{ profile.weight or '-' }} kg</span></div>
        </div>
        {% else %}
            <p>Profil bilgileri yüklenemedi.</p>
        {% endif %}
    </div>

    <h2>💊 İlaç Çizelgesi</h2>
    {% if med_schedules %}
        <table>
            <thead><tr><th>Gün</th><th>İlaç Adı</th><th>Dozaj</th><th>Sıklık</th></tr></thead>
            <tbody>
            {% for s in med_schedules %}
                <tr><td><strong>{{ s.day }}</strong></td><td>{{ s.medication_name }}</td><td>{{ s.dosage }}</td><td>{{ s.frequency }}</td></tr>
            {% endfor %}
            </tbody>
        </table>
    {% else %}
        <div class="empty-msg">Aktif ilaç çizelgesi yok.</div>
    {% endif %}

    <h2>🍽️ Yemek Çizelgesi</h2>
    {% if meal_schedules %}
        <table>
            <thead><tr><th>Gün</th><th>Öğün</th><th>Porsiyon</th></tr></thead>
            <tbody>
            {% for s in meal_schedules %}
                <tr><td><strong>{{ s.day }}</strong></td><td>{{ s.meal_name }}</td><td>{{ s.portion }}</td></tr>
            {% endfor %}
            </tbody>
        </table>
    {% else %}
        <div class="empty-msg">Aktif yemek çizelgesi yok.</div>
    {% endif %}
</div>

</body>
</html>
"""

@app.route('/')
def index():
    patient_id = request.args.get('id', 1, type=int)
    if patient_id is None:
        return render_template_string(HTML_TEMPLATE_PATIENT, patient_id="?", error="ID eksik.", login_url=LOGIN_APP_URL)
        
    med_schedules = []
    meal_schedules = []
    profile = None
    error = None
    
    try:
        # 1. Profil Bilgisini Çek
        user_resp = requests.get(f"{API_BASE_URL}/api/users/{patient_id}")
        if user_resp.status_code == 200:
            profile = user_resp.json()
        
        # 2. İlaç Çizelgesini Çek
        med_resp = requests.get(f"{API_BASE_URL}/api/patient/{patient_id}/schedule/medication")
        if med_resp.status_code == 200: med_schedules = med_resp.json()

        # 3. Yemek Çizelgesini Çek
        meal_resp = requests.get(f"{API_BASE_URL}/api/patient/{patient_id}/schedule/meal")
        if meal_resp.status_code == 200: meal_schedules = meal_resp.json()
        
    except requests.exceptions.RequestException as e:
        error = f"Veriler alınırken hata oluştu: {e}"

    return render_template_string(
        HTML_TEMPLATE_PATIENT, 
        patient_id=patient_id, 
        profile=profile,
        med_schedules=med_schedules, 
        meal_schedules=meal_schedules,
        error=error,
        login_url=LOGIN_APP_URL
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)