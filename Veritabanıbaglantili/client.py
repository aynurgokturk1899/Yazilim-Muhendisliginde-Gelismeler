# client.py (İstemci Uygulaması)
import requests
import json

# API sunucusunun adresi
SERVER_URL = "http://127.0.0.1:5000" 

def client_login(username, password):
    """API'ye giriş yaparak JWT token'ı alır."""
    print(f"\n--- 1. Giriş yapılıyor: {username} ---")
    login_url = f"{SERVER_URL}/login"
    payload = {'username': username, 'password': password}
    
    try:
        response = requests.post(login_url, json=payload)
        response.raise_for_status() # Hata kodu gelirse istisna fırlat

        data = response.json()
        print("✅ Giriş Başarılı. Token Alındı.")
        return data.get('token')
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Giriş başarısız: {response.status_code} - {response.json().get('msg', 'Bilinmeyen hata')}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Sunucuya bağlantı hatası: {e}")
        return None

def access_protected_route(token):
    """Alınan JWT (Bearer Token) ile korumalı rotaya erişir."""
    print("\n--- 2. Korumalı rotaya erişiliyor (Token kullanılarak) ---")
    protected_url = f"{SERVER_URL}/protected"
    
    # Bearer token'ı HTTP başlığına ekle
    headers = {
        'Authorization': f'Bearer {token}'
    }

    try:
        response = requests.get(protected_url, headers=headers)
        response.raise_for_status()

        data = response.json()
        print("✅ Erişim Başarılı.")
        print(json.dumps(data, indent=4, ensure_ascii=False))
        
    except requests.exceptions.HTTPError as e:
        print(f"❌ Erişim başarısız: {response.status_code} - {response.json().get('msg', 'Bilinmeyen hata')}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Sunucuya bağlantı hatası: {e}")


if __name__ == '__main__':
    # Örnek Çalışma Akışı
    
    # A) Başarılı Giriş ve Erişim
    token_alice = client_login('alice', '123456')
    if token_alice:
        access_protected_route(token_alice)
        
    # B) Geçersiz Şifre
    client_login('alice', 'yanlis_sifre')
    
    # C) Token Olmadan Erişim
    print("\n--- 3. Token olmadan erişim deneniyor ---")
    access_protected_route("YANLIS_VEYA_YOK_TOKEN")