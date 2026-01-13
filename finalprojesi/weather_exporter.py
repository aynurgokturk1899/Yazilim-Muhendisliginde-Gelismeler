# weather_exporter.py
from prometheus_client import start_http_server, Gauge
import time
import random

# 81 İlin Listesi
CITIES = [
    "Adana", "Adiyaman", "Afyonkarahisar", "Agri", "Amasya", "Ankara", "Antalya", "Artvin", "Aydin", "Balikesir",
    "Bilecik", "Bingol", "Bitlis", "Bolu", "Burdur", "Bursa", "Canakkale", "Cankiri", "Corum", "Denizli",
    "Diyarbakir", "Edirne", "Elazig", "Erzincan", "Erzurum", "Eskisehir", "Gaziantep", "Giresun", "Gumushane",
    "Hakkari", "Hatay", "Isparta", "Mersin", "Istanbul", "Izmir", "Kars", "Kastamonu", "Kayseri", "Kirklareli",
    "Kirsehir", "Kocaeli", "Konya", "Kutahya", "Malatya", "Manisa", "Kahramanmaras", "Mardin", "Mugla", "Mus",
    "Nevsehir", "Nigde", "Ordu", "Rize", "Sakarya", "Samsun", "Siirt", "Sinop", "Sivas", "Tekirdag", "Tokat",
    "Trabzon", "Tunceli", "Sanliurfa", "Usak", "Van", "Yozgat", "Zonguldak", "Aksaray", "Bayburt", "Karaman",
    "Kirikkale", "Batman", "Sirnak", "Bartin", "Ardahan", "Igdir", "Yalova", "Karabuk", "Kilis", "Osmaniye", "Duzce"
]

# Prometheus Gauge Metriği Tanımlama
# 'turkey_city_temperature' metriğin adıdır, 'city' ise etikettir.
TEMP_GAUGE = Gauge('turkey_city_temperature', 'Turkiye 81 il anlik sicaklik verisi', ['city'])

def generate_weather_data():
    """Her il için rastgele sıcaklık üretir."""
    while True:
        for city in CITIES:
            # -5 ile 35 derece arasında rastgele sıcaklık (Simülasyon)
            temperature = round(random.uniform(-5.0, 35.0), 1)
            TEMP_GAUGE.labels(city=city).set(temperature)
        
        print("Veriler güncellendi...")
        time.sleep(60) # Dakikada bir güncelle

if __name__ == '__main__':
    # Metrics sunucusunu 8000 portunda başlat
    start_http_server(8000)
    print("Prometheus metrics server 8000 portunda calisiyor...")
    generate_weather_data()