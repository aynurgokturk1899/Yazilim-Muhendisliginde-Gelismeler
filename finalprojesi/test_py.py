# test_et.py
from mcp_server import vucut_kitle_indeksi_hesapla, gunluk_motivasyon_sozu_getir

print("--- 1. Hesaplama Testi ---")
# Kilo: 75, Boy: 180 cm
sonuc1 = vucut_kitle_indeksi_hesapla(75, 180)
print(sonuc1)

print("\n--- 2. API Testi (ZenQuotes) ---")
# İnternetten söz getirme
sonuc2 = gunluk_motivasyon_sozu_getir()
print(sonuc2)