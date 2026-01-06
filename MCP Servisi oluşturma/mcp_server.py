from mcp.server.fastmcp import FastMCP
import requests

# Sunucuyu tanımla
mcp = FastMCP("SaglikAsistaniMCP")

# --- TOOL 1: Vücut Kitle İndeksi Hesaplama (İşlem Yapan Tool) ---
@mcp.tool()
def vucut_kitle_indeksi_hesapla(kilo: float, boy_cm: float) -> str:
    """
    Kilo (kg) ve boy (cm) bilgisini alarak Vücut Kitle İndeksini (BMI) hesaplar.
    """
    try:
        if boy_cm <= 0 or kilo <= 0:
            return "Hata: Boy ve kilo pozitif olmalıdır."

        boy_m = boy_cm / 100
        bmi = kilo / (boy_m ** 2)
        bmi_yuvarlanmis = round(bmi, 2)

        durum = ""
        if bmi < 18.5: durum = "Zayıf"
        elif 18.5 <= bmi < 24.9: durum = "Normal"
        elif 25 <= bmi < 29.9: durum = "Fazla Kilolu"
        else: durum = "Obezite"

        return f"BMI: {bmi_yuvarlanmis} - Durum: {durum}"
    except Exception as e:
        return f"Hesaplama hatası: {str(e)}"

# --- TOOL 2: Public API İsteği (Dış Kaynaktan Veri Çeken Tool) ---
@mcp.tool()
def gunluk_motivasyon_sozu_getir() -> str:
    """
    zenquotes.io API'sinden rastgele bir motivasyon sözü getirir.
    (Ödevdeki 'request kullanarak dış sorgu atma' şartını sağlar)
    """
    url = "https://zenquotes.io/api/random"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return f"Günün Sözü: '{data[0]['q']}' - {data[0]['a']}"
        else:
            return "API'ye ulaşılamadı."
    except Exception as e:
        return f"Bağlantı hatası: {str(e)}"

if __name__ == "__main__":
    # MCP sunucusunu başlat
    mcp.run()