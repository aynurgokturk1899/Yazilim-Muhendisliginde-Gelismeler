# flask_projem/dietitian_client.py (GÜNCELLENMİŞ: SINIRSIZ SATIR EKLEME)

from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import requests
import json 

API_BASE_URL = "http://saglik_takip_app:5000"
LOGIN_APP_URL = "http://localhost:5001"

app = Flask(__name__)

HTML_TEMPLATE_DIETITIAN = """
<!doctype html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Diyetisyen Paneli - ID: {{ dietitian_id }}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f1f8f6; color: #333; margin: 0; padding: 0; }
        .container { max-width: 1000px; margin: 30px auto; background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #28a745; padding-bottom: 15px; margin-bottom: 25px; }
        .header h1 { margin: 0; color: #28a745; font-size: 26px; }
        .logout-btn { background-color: #dc3545; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 14px; transition: background 0.3s; }
        
        /* Tablo Stilleri */
        .schedule-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        .schedule-table th, .schedule-table td { border: 1px solid #ddd; padding: 10px; text-align: left; vertical-align: middle; }
        .schedule-table th { background-color: #e8f5e9; color: #2e7d32; font-weight: bold; }
        .schedule-table tr:nth-child(even) { background-color: #fcfcfc; }

        /* Form Elemanları */
        .form-input { width: 95%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        
        /* Kartlar ve Butonlar */
        .patient-card { background: #fff; border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        .flex-row { display: flex; justify-content: space-between; align-items: center; }
        
        button { cursor: pointer; padding: 8px 12px; border: none; border-radius: 4px; font-size: 14px; transition: background 0.3s; }
        .btn-approve { background-color: #007bff; color: white; }
        .btn-action { background-color: #ffc107; color: #333; margin-left: 5px; font-weight: bold; }
        .btn-action:hover { background-color: #e0a800; }
        
        /* Yeni Ekle / Sil Butonları */
        .btn-add-row { background-color: #28a745; color: white; margin-top: 10px; font-weight: bold; }
        .btn-add-row:hover { background-color: #218838; }
        .btn-remove { background-color: #dc3545; color: white; padding: 6px 10px; font-size: 12px; }
        
        .action-area { display: none; margin-top: 15px; background: #f9fff9; border: 1px solid #28a745; padding: 20px; border-radius: 5px; }
        .submit-schedule { background-color: #28a745; color: white; margin-top: 15px; width: 100%; padding: 10px; font-weight: bold; font-size: 16px; }
        .submit-schedule:hover { background-color: #218838; }

        .profile-card { background: #e8f5e9; padding: 15px; border-radius: 6px; margin-bottom: 25px; border: 1px solid #c8e6c9; }
        
        .msg { padding: 10px; margin-bottom: 20px; border-radius: 5px; }
        .success { background-color: #d4edda; color: #155724; }
        .error { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>🥗 Diyetisyen Paneli</h1>
        <a href="{{ login_url }}" class="logout-btn">Çıkış Yap</a>
    </div>

    <div class="profile-card">
        <strong>👤 Diyetisyen:</strong> {{ profile.username if profile else 'Yükleniyor...' }}
    </div>

    {% if message %} <div class="msg success">✅ {{ message }}</div> {% endif %}
    {% if error %} <div class="msg error">❌ {{ error }}</div> {% endif %}

    <h3>Onaylanmış Hastalar</h3>
    {% if approved_patients %}
        <ul>
        {% for patient in approved_patients %}
            <li class="patient-card">
                <div class="flex-row">
                    <strong style="font-size: 18px;">{{ patient.username }}</strong>
                    <div>
                        <button class="btn-action" onclick="toggleForm('meal_form_{{ patient.id }}')">
                            🍽️ Program Düzenle
                        </button>
                    </div>
                </div>

                <div id="meal_form_{{ patient.id }}" class="action-area">
                    <h4 style="margin-top:0; color:#28a745; border-bottom:1px solid #c8e6c9; padding-bottom:10px;">
                        {{ patient.username }} İçin Beslenme Programı
                    </h4>
                    
                    <form method="POST" action="/create_meal_schedule/{{ patient.id }}?id={{ dietitian_id }}">
                        <table class="schedule-table" id="table_{{ patient.id }}">
                            <thead>
                                <tr>
                                    <th style="width: 20%;">Gün</th>
                                    <th style="width: 25%;">Öğün Türü</th>
                                    <th>İçerik / Porsiyon</th>
                                    <th style="width: 10%;">İşlem</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>
                                        <select name="day[]" class="form-input">
                                            <option value="Pazartesi">Pazartesi</option>
                                            <option value="Salı">Salı</option>
                                            <option value="Çarşamba">Çarşamba</option>
                                            <option value="Perşembe">Perşembe</option>
                                            <option value="Cuma">Cuma</option>
                                            <option value="Cumartesi">Cumartesi</option>
                                            <option value="Pazar">Pazar</option>
                                        </select>
                                    </td>
                                    <td>
                                        <select name="meal[]" class="form-input">
                                            <option value="Kahvaltı">Kahvaltı</option>
                                            <option value="Öğle">Öğle</option>
                                            <option value="Akşam">Akşam</option>
                                            <option value="Ara Öğün">Ara Öğün</option>
                                            <option value="Tam Gün">Tam Gün</option>
                                        </select>
                                    </td>
                                    <td>
                                        <input type="text" name="portion[]" class="form-input" placeholder="Örn: 2 Yumurta, Bol Yeşillik" required>
                                    </td>
                                    <td>
                                        <button type="button" class="btn-remove" onclick="removeRow(this)">Sil</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        
                        <button type="button" class="btn-add-row" onclick="addRow('table_{{ patient.id }}')">➕ Yeni Öğün Ekle</button>
                        <br>
                        
                        <button type="submit" class="submit-schedule">💾 Programı Kaydet</button>
                    </form>
                </div>
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p style="color:#777;">Henüz onaylanmış hasta bulunmamaktadır.</p>
    {% endif %}
    
    <hr>
    
    <h3>Onay Bekleyenler</h3>
    {% if pending_patients %}
        <ul>
        {% for p in pending_patients %}
            <li class="patient-card flex-row" style="background:#fff3cd; border-color:#ffeeba;">
                <div><strong>{{ p.username }}</strong></div>
                <form method="POST" action="/approve_patient/{{ p.id }}?id={{ dietitian_id }}" style="margin:0;">
                    <button type="submit" class="btn-approve">✅ Onayla</button>
                </form>
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <small style="color:#777;">Bekleyen istek yok.</small>
    {% endif %}
</div>

<script>
    // Formu açıp kapatma
    function toggleForm(id) {
        var el = document.getElementById(id);
        el.style.display = (el.style.display === 'block') ? 'none' : 'block';
    }

    // Yeni Satır Ekleme
    function addRow(tableId) {
        var table = document.getElementById(tableId).getElementsByTagName('tbody')[0];
        var newRow = table.insertRow();
        newRow.innerHTML = `
            <td>
                <select name="day[]" class="form-input">
                    <option value="Pazartesi">Pazartesi</option>
                    <option value="Salı">Salı</option>
                    <option value="Çarşamba">Çarşamba</option>
                    <option value="Perşembe">Perşembe</option>
                    <option value="Cuma">Cuma</option>
                    <option value="Cumartesi">Cumartesi</option>
                    <option value="Pazar">Pazar</option>
                </select>
            </td>
            <td>
                <select name="meal[]" class="form-input">
                    <option value="Kahvaltı">Kahvaltı</option>
                    <option value="Öğle">Öğle</option>
                    <option value="Akşam">Akşam</option>
                    <option value="Ara Öğün">Ara Öğün</option>
                    <option value="Tam Gün">Tam Gün</option>
                </select>
            </td>
            <td>
                <input type="text" name="portion[]" class="form-input" placeholder="İçerik giriniz..." required>
            </td>
            <td>
                <button type="button" class="btn-remove" onclick="removeRow(this)">Sil</button>
            </td>
        `;
    }

    // Satır Silme
    function removeRow(btn) {
        var row = btn.parentNode.parentNode;
        row.parentNode.removeChild(row);
    }
</script>

</body>
</html>
"""

@app.route('/')
def index():
    dietitian_id = request.args.get('id', 3, type=int) 
    if dietitian_id is None:
        return render_template_string(HTML_TEMPLATE_DIETITIAN, dietitian_id="?", error="Giriş ID'si eksik.", login_url=LOGIN_APP_URL)

    pending_patients = []
    approved_patients = []
    profile = None
    message = request.args.get('message')
    error = request.args.get('error')
    
    try:
        try:
            user_resp = requests.get(f"{API_BASE_URL}/api/users/{dietitian_id}")
            if user_resp.status_code == 200: profile = user_resp.json()
        except: pass

        pending_resp = requests.get(f"{API_BASE_URL}/api/dietitian/{dietitian_id}/patients/pending")
        if pending_resp.status_code == 200: pending_patients = pending_resp.json()
        
        approved_resp = requests.get(f"{API_BASE_URL}/api/dietitian/{dietitian_id}/patients/approved")
        if approved_resp.status_code == 200: approved_patients = approved_resp.json()

    except requests.exceptions.RequestException as e:
        error = f"API Hatası: {e}"

    return render_template_string(
        HTML_TEMPLATE_DIETITIAN, 
        dietitian_id=dietitian_id, 
        profile=profile,
        pending_patients=pending_patients, 
        approved_patients=approved_patients,
        message=message,
        error=error,
        login_url=LOGIN_APP_URL
    )

@app.route('/approve_patient/<int:patient_id>', methods=['POST'])
def approve_patient_route(patient_id):
    dietitian_id = request.args.get('id', type=int)
    try:
        requests.post(f"{API_BASE_URL}/api/dietitian/{dietitian_id}/patients/approve/{patient_id}").raise_for_status()
        return redirect(url_for('index', id=dietitian_id, message="Hasta onaylandı!"))
    except Exception as e:
        return redirect(url_for('index', id=dietitian_id, error=str(e)))

@app.route('/create_meal_schedule/<int:patient_id>', methods=['POST'])
def create_meal_schedule(patient_id):
    dietitian_id = request.args.get('id', type=int)
    try:
        days = request.form.getlist('day[]')
        meals = request.form.getlist('meal[]')
        portions = request.form.getlist('portion[]')

        schedule_data = []
        for i in range(len(days)):
            # İçerik boş değilse kaydet
            if portions[i].strip():
                schedule_data.append({
                    "day": days[i],
                    "meal": meals[i],
                    "portion": portions[i]
                })
        
        requests.post(f"{API_BASE_URL}/api/dietitian/{dietitian_id}/patient/{patient_id}/schedule/meal", json=schedule_data).raise_for_status()
        
        return redirect(url_for('index', id=dietitian_id, message="Yemek programı başarıyla kaydedildi!"))
    except Exception as e:
        return redirect(url_for('index', id=dietitian_id, error=str(e)))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)