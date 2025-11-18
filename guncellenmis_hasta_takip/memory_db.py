# memory_db.py (GÜNCELLENDİ)

# --- Hafızada (In-Memory) Veri Deposu ---

# Kullanıcılar: ID'leri anahtar (key) olarak kullanılır
USERS = {
    1: {
        "id": 1,
        "username": "hasta_ahmet",
        "role": "patient",
        "password": "pass", # Giriş için basit parola (Gerçekte hashlenmeli)
        "email": "ahmet@mail.com",
        "tc_kimlik": "11111111111",
        "birth_date": "1990-01-01",
        "gender": "Erkek",
        "height": 180,
        "weight": 80,
        "selected_doctor_id": 2, # Hasta tarafından seçildi
        "selected_dietitian_id": 3 # Hasta tarafından seçildi
    },
    2: {
        "id": 2,
        "username": "doktor_zeynep",
        "role": "doctor",
        "password": "pass",
        "email": "zeynep@hastane.com",
        "tc_kimlik": "22222222222",
        "birth_date": "1985-05-15",
        "gender": "Kadın",
        "hospital": "Şehir Hastanesi",
        "phone": "5551234567"
    },
    3: {
        "id": 3,
        "username": "diyetisyen_can",
        "role": "dietitian",
        "password": "pass",
        "email": "can@saglik.com",
        "tc_kimlik": "33333333333",
        "birth_date": "1992-11-20",
        "gender": "Erkek",
        "hospital": "Sağlık Merkezi",
        "phone": "5559876543"
    }
}
_user_id_counter = 4

# Hasta-Klinisyen İlişkileri (Onay sistemi)
LINKS = [
    {
        "id": 1,
        "patient_id": 1,
        "clinician_id": 2, # Doktor Zeynep
        "is_approved": False # Onay bekleniyor
    },
    {
        "id": 2,
        "patient_id": 1,
        "clinician_id": 3, # Diyetisyen Can
        "is_approved": True # Onaylanmış
    }
]
_link_id_counter = 3

# Çizelgeler
MED_SCHEDULES = []
_med_id_counter = 1

MEAL_SCHEDULES = [
    {
        "id": 1,
        "patient_id": 1,
        "dietitian_id": 3,
        "day": "Pazartesi",
        "meal": "Kahvaltı",
        "portion": "1 dilim peynir, 5 zeytin"
    }
]
_meal_id_counter = 2

# --- Yardımcı Fonksiyonlar (ID yönetimi ve Veri Yönetimi için) ---

def get_next_id(counter_name):
    global _user_id_counter, _link_id_counter, _med_id_counter, _meal_id_counter
    
    if counter_name == 'user':
        id = _user_id_counter
        _user_id_counter += 1
    elif counter_name == 'link':
        id = _link_id_counter
        _link_id_counter += 1
    elif counter_name == 'med':
        id = _med_id_counter
        _med_id_counter += 1
    elif counter_name == 'meal':
        id = _meal_id_counter
        _meal_id_counter += 1
    else:
        raise ValueError("Geçersiz sayaç adı")
    
    return id

def get_next_med_id():
    return get_next_id('med')

def get_next_meal_id():
    return get_next_id('meal')

def get_next_user_id():
    return get_next_id('user')

def get_next_link_id():
    return get_next_id('link')