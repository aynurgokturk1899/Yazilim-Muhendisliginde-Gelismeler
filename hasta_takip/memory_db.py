# --- Hafızada (In-Memory) Veri Deposu ---
# Sunucu yeniden başladığında bu veriler sıfırlanır.

# Kullanıcılar: ID'leri anahtar (key) olarak kullanılır
USERS = {
    1: {
        "id": 1,
        "username": "hasta_ahmet",
        "role": "patient",
        "tc_kimlik": "11111111111",
        "birth_date": "1990-01-01",
        "height": 180,
        "weight": 80
    },
    2: {
        "id": 2,
        "username": "doktor_zeynep",
        "role": "doctor",
        "tc_kimlik": "22222222222",
        "hospital": "Şehir Hastanesi"
    },
    3: {
        "id": 3,
        "username": "diyetisyen_can",
        "role": "dietitian",
        "tc_kimlik": "33333333333",
        "hospital": "Sağlık Merkezi"
    }
}
_user_id_counter = 4 # Bir sonraki kullanıcı ID'si

# Hasta-Klinisyen İlişkileri (Onay sistemi)
LINKS = [
    {
        "id": 1,
        "patient_id": 1,       # hasta_ahmet
        "clinician_id": 2,     # doktor_zeynep
        "is_approved": False   # Henüz onaylanmamış
    },
    {
        "id": 2,
        "patient_id": 1,       # hasta_ahmet
        "clinician_id": 3,     # diyetisyen_can
        "is_approved": True    # Onaylanmış
    }
]
_link_id_counter = 3

# Çizelgeler
MED_SCHEDULES = [] # Doktorlar dolduracak
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

# --- Yardımcı Fonksiyonlar (ID yönetimi için) ---
def get_next_med_id():
    global _med_id_counter
    id = _med_id_counter
    _med_id_counter += 1
    return id

def get_next_meal_id():
    global _meal_id_counter
    id = _meal_id_counter
    _meal_id_counter += 1
    return id