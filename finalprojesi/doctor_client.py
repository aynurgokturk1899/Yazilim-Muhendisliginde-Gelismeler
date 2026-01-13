# flask_projem/doctor_client.py (SINIRSIZ EKLEME ÖZELLİKLİ)

from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import requests 
import json 

API_BASE_URL = "http://saglik_takip_app:5000"
LOGIN_APP_URL = "http://localhost:5001"

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>Doktor Paneli - ID: {{ doctor_id }}</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; color: #333; margin: 0; padding: 0; }
        .container { max-width: 1000px; margin: 30px auto; background: #fff; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #007bff; padding-bottom: 15px; margin-bottom: 25px; }
        .header h1 { margin: 0; color: #007bff; font-size: 26px; }
        .logout-btn { background-color: #dc3545; color: white; padding: 8px 16px; text-decoration: none; border-radius: 4px; font-weight: bold; font-size: 14px; transition: background 0.3s;}
        
        /* Tablo Stilleri */
        .schedule-table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        .schedule-table th, .schedule-table td { border: 1px solid #ddd; padding: 10px; text-align: left; vertical-align: middle; }
        .schedule-table th { background-color: #f1f8ff; color: #007bff; font-weight: bold; }
        .schedule-table tr:nth-child(even) { background-color: #f9f9f9; }
        
        .form-input { width: 90%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
        
        .patient-card { background: #fff; border: 1px solid #e1e1e1; padding: 15px; margin-bottom: 15px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }
        button { cursor: pointer; padding: 8px 12px; border: none; border-radius: 4px; font-size: 14px; transition: 0.3s; }
        .btn-approve { background-color: #28a745; color: white; }
        .btn-edit { background-color: #17a2b8; color: white; float: right; }
        
        /* Yeni Butonlar */
        .btn-add-row { background-color: #28a745; color: white; margin-top: 10px; font-weight: bold; }
        .btn-add-row:hover { background-color: #218838; }
        .btn-remove { background-color: #dc3545; color: white; padding: 5px 10px; font-size: 12px; }
        
        .action-area { display: none; margin-top: 15px; background: white; border: 1px solid #17a2b8; padding: 20px; border-radius: 5px; }
        .submit-schedule { background-color: #007bff; color: white; margin-top: 15px; width: 100%; padding: 12px; font-size: 16px; font-weight: bold; }
        
        .msg { padding: 10px; margin-bottom: 10px; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; } .error { background: #f8d7da; color: #721c24; }
        .profile-card { background: #e3f2fd; padding: 15px; border-radius: 6px; margin-bottom: 25px; border: 1px solid #bbdefb; }
    </style>
</head>
<body>

<div class="container">
    <div class="header">
        <h1>👨‍⚕️ Doktor Paneli</h1>
        <a href="{{ login_url }}" class="logout-btn">Çıkış Yap</a>
    </div>

    <div class="profile-card">
        <strong>👤 Doktor:</strong> {{ profile.username if profile else 'Yükleniyor...' }}
    </div>

    {% if message %} <div class="msg success">✅ {{ message }}</div> {% endif %}
    {% if error %} <div class="msg error">⚠️ {{ error }}</div> {% endif %}

    <h3>Onaylanmış Hastalar</h3>
    {% if approved_patients %}
        <ul>
        {% for p in approved_patients %}
            <li class="patient-card">
                <div style="overflow: hidden;">
                    <strong style="font-size: 18px;">{{ p.username }}</strong>
                    <button class="btn-edit" onclick="toggleForm('form_{{ p.id }}')">
                        ✏️ İlaç Çizelgesi Düzenle
                    </button>
                </div>
                
                <div id="form_{{ p.id }}" class="action-area">
                    <h4 style="margin-top:0; color:#17a2b8; border-bottom:1px solid #eee; padding-bottom:10px;">
                        {{ p.username }} İçin İlaç Planı
                    </h4>
                    
                    <form method="POST" action="/create_schedule/{{ p.id }}?id={{ doctor_id }}">
                        <table class="schedule-table" id="table_{{ p.id }}">
                            <thead>
                                <tr>
                                    <th style="width: 20%;">Gün</th>
                                    <th style="width: 25%;">İlaç Adı</th>
                                    <th style="width: 20%;">Dozaj</th>
                                    <th style="width: 25%;">Sıklık</th>
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
                                    <td><input type="text" name="medication[]" class="form-input" placeholder="İlaç adı" required></td>
                                    <td><input type="text" name="dosage[]" class="form-input" placeholder="Örn: 100mg"></td>
                                    <td>
                                        <select name="frequency[]" class="form-input">
                                            <option value="Sabah">Sabah</option>
                                            <option value="Akşam">Akşam</option>
                                            <option value="Sabah-Akşam">Sabah-Akşam</option>
                                            <option value="Günde 3 Kez">Günde 3 Kez</option>
                                            <option value="Gece">Gece</option>
                                        </select>
                                    </td>
                                    <td><button type="button" class="btn-remove" onclick="removeRow(this)">Sil</button></td>
                                </tr>
                            </tbody>
                        </table>
                        
                        <button type="button" class="btn-add-row" onclick="addRow('table_{{ p.id }}')">➕ Yeni İlaç Ekle</button>
                        <br>
                        <button type="submit" class="submit-schedule">💾 Tümünü Kaydet</button>
                    </form>
                </div>
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p style="color:#777;">Henüz onaylanmış hasta yok.</p>
    {% endif %}

    <hr>
    <h3>Onay Bekleyenler</h3>
    {% if pending_patients %}
        <ul>
        {% for p in pending_patients %}
            <li class="patient-card">
                <strong>{{ p.username }}</strong> 
                <form method="POST" action="/approve_patient/{{ p.id }}?id={{ doctor_id }}" style="display:inline; float:right;">
                    <button type="submit" class="btn-approve">✅ Onayla</button>
                </form>
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p style="color:#777;">Bekleyen istek yok.</p>
    {% endif %}
</div>

<script>
    function toggleForm(id) {
        var el = document.getElementById(id);
        el.style.display = (el.style.display === 'block') ? 'none' : 'block';
    }

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
            <td><input type="text" name="medication[]" class="form-input" placeholder="İlaç adı" required></td>
            <td><input type="text" name="dosage[]" class="form-input" placeholder="Örn: 100mg"></td>
            <td>
                <select name="frequency[]" class="form-input">
                    <option value="Sabah">Sabah</option>
                    <option value="Akşam">Akşam</option>
                    <option value="Sabah-Akşam">Sabah-Akşam</option>
                    <option value="Günde 3 Kez">Günde 3 Kez</option>
                    <option value="Gece">Gece</option>
                </select>
            </td>
            <td><button type="button" class="btn-remove" onclick="removeRow(this)">Sil</button></td>
        `;
    }

    function removeRow(btn) {
        var row = btn.parentNode.parentNode;
        // En az bir satır kalsın istiyorsak bu kontrolü açabiliriz, şimdilik serbest bırakıyoruz.
        row.parentNode.removeChild(row);
    }
</script>
</body>
</html>
"""

@app.route('/')
def index():
    doctor_id = request.args.get('id', 2, type=int) 
    
    pending_patients = []
    approved_patients = []
    profile = None
    msg = request.args.get('message')
    err = request.args.get('error')
    
    try:
        try:
            user_resp = requests.get(f"{API_BASE_URL}/api/users/{doctor_id}")
            if user_resp.status_code == 200: profile = user_resp.json()
        except: pass

        pending_patients = requests.get(f"{API_BASE_URL}/api/doctor/{doctor_id}/patients/pending").json()
        approved_patients = requests.get(f"{API_BASE_URL}/api/doctor/{doctor_id}/patients/approved").json()
    except Exception as e:
        err = f"API Bağlantı Hatası: {e}"

    return render_template_string(HTML_TEMPLATE, doctor_id=doctor_id, profile=profile, pending_patients=pending_patients, approved_patients=approved_patients, message=msg, error=err, login_url=LOGIN_APP_URL)

@app.route('/approve_patient/<int:patient_id>', methods=['POST'])
def approve_patient_route(patient_id):
    doctor_id = request.args.get('id')
    try:
        requests.post(f"{API_BASE_URL}/api/doctor/{doctor_id}/patients/approve/{patient_id}").raise_for_status()
        return redirect(url_for('index', id=doctor_id, message="Hasta onaylandı"))
    except Exception as e:
        return redirect(url_for('index', id=doctor_id, error=str(e)))

@app.route('/create_schedule/<int:patient_id>', methods=['POST'])
def create_schedule(patient_id):
    doctor_id = request.args.get('id')
    try:
        days = request.form.getlist('day[]')
        meds = request.form.getlist('medication[]')
        dosages = request.form.getlist('dosage[]')
        freqs = request.form.getlist('frequency[]')

        schedule_data = []
        for i in range(len(days)):
            if meds[i].strip(): # İlaç adı boş değilse kaydet
                schedule_data.append({
                    "day": days[i],
                    "medication": meds[i],
                    "dosage": dosages[i],
                    "frequency": freqs[i]
                })

        requests.post(f"{API_BASE_URL}/api/doctor/{doctor_id}/patient/{patient_id}/schedule/medication", json=schedule_data).raise_for_status()
        
        return redirect(url_for('index', id=doctor_id, message="Çizelge kaydedildi!"))
    except Exception as e:
        return redirect(url_for('index', id=doctor_id, error=f"Hata: {str(e)}"))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)